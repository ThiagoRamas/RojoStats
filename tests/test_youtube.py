import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import requests

from youtube_service.client import YouTubeAPIError, obtener_rendimiento_videos


class YouTubeVideosTests(unittest.TestCase):
    @patch("youtube_service.client.requests.get")
    def test_ultimo_video_y_mas_visto_del_mes(self, get: Mock) -> None:
        respuesta_playlist = Mock()
        respuesta_playlist.json.return_value = {
            "items": [
                {"contentDetails": {"videoId": "nuevo"}},
                {"contentDetails": {"videoId": "popular"}},
                {"contentDetails": {"videoId": "viejo"}},
            ]
        }
        respuesta_playlist.raise_for_status.return_value = None
        respuesta_videos = Mock()
        respuesta_videos.json.return_value = {"items": [
            {
                "id": "nuevo",
                "snippet": {"title": "Último", "publishedAt": "2026-07-31T12:00:00Z"},
                "statistics": {"viewCount": "100", "likeCount": "10"},
            },
            {
                "id": "popular",
                "snippet": {"title": "Popular", "publishedAt": "2026-07-15T12:00:00Z"},
                "statistics": {"viewCount": "500", "commentCount": "20"},
            },
            {
                "id": "viejo",
                "snippet": {"title": "Viejo", "publishedAt": "2026-06-01T12:00:00Z"},
                "statistics": {"viewCount": "1000"},
            },
        ]}
        respuesta_videos.raise_for_status.return_value = None
        get.side_effect = [respuesta_playlist, respuesta_videos]

        resultado = obtener_rendimiento_videos(
            "uploads",
            datetime(2026, 8, 1, tzinfo=timezone.utc),
        )

        self.assertEqual(resultado["ultimo"]["id"], "nuevo")
        self.assertEqual(resultado["mas_visto_30_dias"]["id"], "popular")
        self.assertEqual(resultado["publicados_30_dias"], 2)
        self.assertIsNone(resultado["ultimo"]["comentarios"])

    @patch("youtube_service.client.requests.get")
    def test_el_error_no_expone_la_clave_api(self, get: Mock) -> None:
        get.side_effect = requests.ConnectionError(
            "https://example.test?key=clave-secreta"
        )

        with self.assertRaises(YouTubeAPIError) as contexto:
            obtener_rendimiento_videos("uploads")

        self.assertNotIn("clave-secreta", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
