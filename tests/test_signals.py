import unittest

from analytics.signals import calcular_senales


def comparacion(
    suscriptores: float,
    visualizaciones: float,
    videos: int = 0,
) -> dict:
    return {
        "suscriptores": 0,
        "visualizaciones": 0,
        "videos": videos,
        "promedios_diarios": {
            "suscriptores": suscriptores,
            "visualizaciones": visualizaciones,
            "videos": 0,
        },
    }


class SignalsTests(unittest.TestCase):
    def test_detecta_publicacion_y_aceleracion(self) -> None:
        estadisticas = {"rendimiento_videos": {}}
        comparaciones = {
            "hoy": comparacion(0, 0, videos=1),
            "7_dias": comparacion(20, 2000),
            "30_dias": comparacion(10, 1000),
        }

        senales = calcular_senales(estadisticas, comparaciones)

        self.assertIn("🎬 1 video nuevo publicado hoy.", senales)
        self.assertTrue(any("suscriptores" in senal for senal in senales))
        self.assertTrue(any("visualizaciones" in senal for senal in senales))

    def test_no_inventa_tendencias_sin_historial(self) -> None:
        senales = calcular_senales(
            {"rendimiento_videos": {}},
            {"hoy": None, "7_dias": None, "30_dias": None},
        )

        self.assertEqual(senales, [])

    def test_ultimo_video_lidera_el_mes(self) -> None:
        video = {"id": "abc"}
        estadisticas = {"rendimiento_videos": {
            "ultimo": video,
            "mas_visto_30_dias": video,
            "publicados_30_dias": 3,
        }}

        senales = calcular_senales(
            estadisticas,
            {"hoy": None, "7_dias": None, "30_dias": None},
        )

        self.assertIn(
            "🔥 El último video es el más visto de los últimos 30 días.",
            senales,
        )


if __name__ == "__main__":
    unittest.main()
