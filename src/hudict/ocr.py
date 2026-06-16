import asyncio
import io
import re

from PIL import Image
from winsdk.windows.globalization import Language
from winsdk.windows.graphics.imaging import BitmapDecoder
from winsdk.windows.media.ocr import OcrEngine
from winsdk.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

from hudict.models import Box, Line, Word

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'’-]*")


class WindowsOcr:
    def __init__(self):
        self.engine = OcrEngine.try_create_from_language(Language("en-US"))
        if not self.engine:
            self.engine = OcrEngine.try_create_from_user_profile_languages()
        if not self.engine:
            raise RuntimeError("Windows OCR English engine is not available.")

    def scan(self, image: Image.Image):
        try:
            return asyncio.run(self._scan_async(image))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._scan_async(image))
            finally:
                loop.close()

    async def _scan_async(self, image):
        bitmap = await self._pil_to_bitmap(image)
        result = await self.engine.recognize_async(bitmap)
        lines = []
        for raw_line in result.lines:
            words = []
            for raw_word in raw_line.words:
                text = raw_word.text.strip()
                if not WORD_RE.fullmatch(text):
                    continue
                rect = raw_word.bounding_rect
                words.append(Word(text=text, box=Box(rect.x, rect.y, rect.width, rect.height)))
            if not words:
                continue
            lines.append(Line(text=raw_line.text, words=words, box=self._merge_boxes([word.box for word in words])))
        return lines

    async def _pil_to_bitmap(self, image):
        with io.BytesIO() as bio:
            image.convert("RGB").save(bio, format="PNG")
            data = bio.getvalue()

        stream = InMemoryRandomAccessStream()
        writer = DataWriter(stream.get_output_stream_at(0))
        writer.write_bytes(data)
        await writer.store_async()
        await writer.flush_async()
        writer.detach_stream()
        stream.seek(0)
        decoder = await BitmapDecoder.create_async(stream)
        return await decoder.get_software_bitmap_async()

    def _merge_boxes(self, boxes):
        left = min(box.left for box in boxes)
        top = min(box.top for box in boxes)
        right = max(box.right for box in boxes)
        bottom = max(box.bottom for box in boxes)
        return Box(left, top, right - left, bottom - top)
