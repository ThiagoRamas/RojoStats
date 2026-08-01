import unittest
from datetime import datetime, timedelta, timezone

from storage.history import calcular_comparaciones, crear_medicion


class HistoryTests(unittest.TestCase):
    def test_calcula_hoy_semana_y_mes(self) -> None:
        ahora = datetime(2026, 8, 1, 15, tzinfo=timezone.utc)
        base = {"suscriptores": 100, "visualizaciones": 1000, "videos": 10}
        historial = [
            crear_medicion(base, ahora - timedelta(days=31)),
            crear_medicion({**base, "suscriptores": 120}, ahora - timedelta(days=8)),
            crear_medicion({**base, "suscriptores": 130}, ahora.replace(hour=1)),
        ]
        actuales = {**base, "suscriptores": 140}

        resultado = calcular_comparaciones(historial, actuales, ahora)

        self.assertEqual(resultado["hoy"]["suscriptores"], 10)
        self.assertEqual(resultado["7_dias"]["suscriptores"], 20)
        self.assertEqual(resultado["30_dias"]["suscriptores"], 40)
        self.assertAlmostEqual(
            resultado["7_dias"]["porcentajes"]["suscriptores"],
            100 / 6,
        )
        self.assertAlmostEqual(
            resultado["7_dias"]["promedios_diarios"]["suscriptores"],
            2.5,
        )

    def test_no_inventa_periodos_sin_historial(self) -> None:
        ahora = datetime(2026, 8, 1, 15, tzinfo=timezone.utc)
        historial = [crear_medicion(
            {"suscriptores": 100, "visualizaciones": 1000, "videos": 10},
            ahora.replace(hour=1),
        )]
        actuales = {"suscriptores": 110, "visualizaciones": 1100, "videos": 11}

        resultado = calcular_comparaciones(historial, actuales, ahora)

        self.assertEqual(resultado["hoy"]["suscriptores"], 10)
        self.assertIsNone(resultado["7_dias"])
        self.assertIsNone(resultado["30_dias"])

    def test_porcentaje_indisponible_si_la_referencia_es_cero(self) -> None:
        ahora = datetime(2026, 8, 1, 15, tzinfo=timezone.utc)
        base = {"suscriptores": 0, "visualizaciones": 0, "videos": 0}
        historial = [crear_medicion(base, ahora - timedelta(days=8))]
        actuales = {"suscriptores": 10, "visualizaciones": 100, "videos": 1}

        resultado = calcular_comparaciones(historial, actuales, ahora)

        self.assertIsNone(resultado["7_dias"]["porcentajes"]["suscriptores"])


if __name__ == "__main__":
    unittest.main()
