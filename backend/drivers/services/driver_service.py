from drivers.models import Driver


class DriverService:
    """
    Contiene las operaciones de negocio relacionadas con conductores.
    """

    @staticmethod
    def find_active_driver_by_identification(
        identification_number: str,
    ) -> Driver | None:
        """
        Busca un conductor activo utilizando su número de identificación.

        Retorna:
        - Driver si existe y está activo.
        - None si no existe o está inactivo.
        """

        return Driver.objects.filter(
            identification_number=identification_number,
            is_active=True,
        ).first()