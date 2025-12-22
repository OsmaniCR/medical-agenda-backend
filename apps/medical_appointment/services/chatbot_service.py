import json
import logging
from typing import Optional, List, Dict, Any
from django.conf import settings
from django.contrib.auth.models import User
from openai import OpenAI
from ..models import MedicalAppointment

logger = logging.getLogger(__name__)


class ChatbotService:
    """Servicio para manejar la lógica del chatbot de agendamiento médico"""

    def __init__(self):
        """Inicializa el cliente de OpenAI"""
        self.client = self._initialize_openai_client()

    def _initialize_openai_client(self) -> Optional[OpenAI]:
        """Inicializa y valida el cliente de OpenAI"""
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.strip():
            logger.warning("OPENAI_API_KEY no está configurada")
            return None

        api_key = settings.OPENAI_API_KEY.strip()
        if not api_key.startswith("sk-"):
            logger.warning(
                "OPENAI_API_KEY no tiene el formato correcto (debe empezar con 'sk-')"
            )
            return None

        return OpenAI(api_key=api_key)

    def _get_appointments(self, user: User) -> List[Dict[str, Any]]:
        """Obtiene todas las citas del usuario"""
        appointments = MedicalAppointment.objects.filter(patient=user)
        return [
            {
                "id": apt.id,
                "date": str(apt.date),
                "time": str(apt.time),
                "reason": apt.reason,
                "status": apt.status,
            }
            for apt in appointments
        ]

    def _create_appointment(
        self,
        user: User,
        date: str,
        time: str,
        reason: str,
    ) -> Dict[str, Any]:
        """Crea una nueva cita médica para el usuario"""
        appointment = MedicalAppointment.objects.create(
            patient=user,
            date=date,
            time=time,
            reason=reason,
            status="pending",
        )
        return {
            "id": appointment.id,
            "date": str(appointment.date),
            "time": str(appointment.time),
            "reason": appointment.reason,
            "status": appointment.status,
        }

    def _update_appointment(
        self,
        user: User,
        appointment_id: int,
        date: Optional[str] = None,
        time: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Actualiza una cita médica existente"""
        try:
            appointment = MedicalAppointment.objects.get(
                id=appointment_id, patient=user
            )
        except MedicalAppointment.DoesNotExist:
            return {"error": "Appointment not found"}

        if date:
            appointment.date = date
        if time:
            appointment.time = time
        if reason:
            appointment.reason = reason

        appointment.save()
        return {
            "id": appointment.id,
            "date": str(appointment.date),
            "time": str(appointment.time),
            "reason": appointment.reason,
            "status": appointment.status,
        }

    def _delete_appointment(self, user: User, appointment_id: int) -> Dict[str, Any]:
        """Elimina una cita médica"""
        try:
            appointment = MedicalAppointment.objects.get(
                id=appointment_id, patient=user
            )
            appointment.delete()
            return {"success": True, "message": "Appointment deleted successfully"}
        except MedicalAppointment.DoesNotExist:
            return {"error": "Appointment not found"}

    def _get_tools(self) -> List[Dict[str, Any]]:
        """Retorna la definición de las herramientas (tools) para OpenAI"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_appointments",
                    "description": "Obtiene todas las citas médicas del usuario. Úsalo cuando el usuario pregunte por sus citas, quiera verlas o listarlas.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_appointment",
                    "description": "Crea una nueva cita médica para el paciente autenticado. Acepta fechas y horas en lenguaje natural (ej: '2 de julio de 2026', '3 de la tarde', '15:30'). Debes convertir automáticamente a formato YYYY-MM-DD para fecha y HH:MM para hora antes de llamar esta función.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Fecha de la cita. Debes convertir cualquier formato de fecha (ej: '2 de julio de 2026', '15/03/2025', 'mañana') a formato YYYY-MM-DD antes de pasar este parámetro.",
                            },
                            "time": {
                                "type": "string",
                                "description": "Hora de la cita. Debes convertir cualquier formato de hora (ej: '3 de la tarde', '3 PM', '15:00', 'tres de la tarde') a formato HH:MM en 24 horas antes de pasar este parámetro.",
                            },
                            "reason": {
                                "type": "string",
                                "description": "Motivo o razón de la cita médica",
                            },
                        },
                        "required": ["date", "time", "reason"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "update_appointment",
                    "description": "Actualiza una cita médica existente. Requiere el ID de la cita y los campos a actualizar (fecha, hora o motivo).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID de la cita médica a actualizar",
                            },
                            "date": {
                                "type": "string",
                                "description": "Nueva fecha. Debes convertir cualquier formato de fecha a YYYY-MM-DD antes de pasar este parámetro (opcional)",
                            },
                            "time": {
                                "type": "string",
                                "description": "Nueva hora. Debes convertir cualquier formato de hora a HH:MM en 24 horas antes de pasar este parámetro (opcional)",
                            },
                            "reason": {
                                "type": "string",
                                "description": "Nuevo motivo (opcional)",
                            },
                        },
                        "required": ["appointment_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_appointment",
                    "description": "Elimina una cita médica. Requiere el ID de la cita.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID de la cita médica a eliminar",
                            },
                        },
                        "required": ["appointment_id"],
                    },
                },
            },
        ]

    def _get_system_message(self) -> str:
        """Retorna el mensaje del sistema para el chatbot"""
        return """Eres un asistente virtual EXCLUSIVAMENTE para agendamiento médico. Tu única función es ayudar a los usuarios a gestionar sus citas médicas mediante las siguientes acciones:

ACCIONES DISPONIBLES:
- Agendar nuevas citas médicas
- Consultar y listar citas existentes
- Modificar citas existentes
- Eliminar citas

IMPORTANTE - FORMATOS DE FECHA Y HORA:
- Acepta fechas y horas en CUALQUIER formato natural que el usuario use (ej: "2 de julio de 2026", "15/03/2025", "mañana", "el próximo lunes").
- Acepta horas en formato natural (ej: "3 de la tarde", "3 PM", "15:30", "tres de la tarde", "las 3 PM").
- DEBES convertir automáticamente estas fechas y horas a los formatos requeridos (YYYY-MM-DD para fecha, HH:MM en 24 horas para hora) ANTES de llamar a las funciones.
- NUNCA pidas al usuario que use formatos específicos. Simplemente acepta lo que diga y conviértelo automáticamente.
- Si hay ambigüedad en la fecha u hora, usa tu mejor criterio o pregunta de manera natural (ej: "¿Te refieres a las 3 de la tarde o de la mañana?").

REGLAS ESTRICTAS:
1. SOLO puedes responder preguntas y realizar acciones relacionadas con citas médicas.
2. NO debes responder preguntas sobre ningún otro tema que no esté relacionado con citas médicas.
3. Si recibes una pregunta que NO está relacionada con citas médicas, debes responder de manera amable pero firme:
   "Lo siento, soy un asistente especializado únicamente en la gestión de citas médicas. Solo puedo ayudarte con:
   - Agendar nuevas citas médicas
   - Consultar tus citas existentes
   - Modificar citas
   - Eliminar citas
   ¿En qué puedo ayudarte con tus citas médicas?"

Sé amable, profesional y claro en tus respuestas. Cuando uses las funciones, explica claramente lo que estás haciendo.

Cuando muestres listas de citas médicas, formatea cada cita de manera clara y estructurada usando el siguiente formato:

📅 **Cita #{id}**
- 📆 Fecha: {fecha formateada en español}
- ⏰ Hora: {hora}
- 📝 Motivo: {motivo}
- ✅ Estado: {estado traducido al español}

Si hay múltiples citas, numéralas y sepáralas con una línea en blanco. Usa emojis para hacer la información más visual y fácil de leer. Las fechas deben mostrarse en formato legible en español (ej: "22 de diciembre de 2025"). Los estados deben traducirse: "pending" → "Pendiente", "confirmed" → "Confirmada", "cancelled" → "Cancelada"."""

    def _execute_tool_call(
        self, user: User, function_name: str, function_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta una llamada a función (tool call) del chatbot"""
        if function_name == "get_appointments":
            return self._get_appointments(user)
        elif function_name == "create_appointment":
            return self._create_appointment(
                user,
                function_args.get("date"),
                function_args.get("time"),
                function_args.get("reason"),
            )
        elif function_name == "update_appointment":
            return self._update_appointment(
                user,
                function_args.get("appointment_id"),
                function_args.get("date"),
                function_args.get("time"),
                function_args.get("reason"),
            )
        elif function_name == "delete_appointment":
            return self._delete_appointment(user, function_args.get("appointment_id"))
        else:
            return {"error": "Unknown function"}

    def get_response(
        self,
        user: User,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Genera una respuesta del chatbot usando OpenAI con tool calling

        Args:
            user: Usuario autenticado
            message: Mensaje del usuario
            conversation_history: Historial de conversación (opcional)

        Returns:
            Respuesta del chatbot

        Raises:
            ValueError: Si la API key no está configurada o el mensaje está vacío
        """
        if not self.client:
            raise ValueError(
                "OpenAI API key no está configurada. Por favor, configura OPENAI_API_KEY en el archivo .env"
            )

        if not message or not message.strip():
            raise ValueError("El mensaje no puede estar vacío")

        api_key = settings.OPENAI_API_KEY.strip()
        if not api_key.startswith("sk-"):
            raise ValueError(
                "La API key de OpenAI no tiene el formato correcto. Debe empezar con 'sk-'"
            )

        tools = self._get_tools()
        messages = [{"role": "system", "content": self._get_system_message()}]

        if conversation_history:
            for msg in conversation_history:
                if (
                    not isinstance(msg, dict)
                    or "role" not in msg
                    or "content" not in msg
                ):
                    logger.warning(f"Mensaje inválido en conversation_history: {msg}")
                    continue
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
            )
        except Exception as e:
            error_str = str(e)
            logger.error(f"Error al llamar a OpenAI: {error_str}")

            if (
                "401" in error_str
                or "invalid_api_key" in error_str.lower()
                or "authentication" in error_str.lower()
            ):
                raise ValueError(
                    "La API key de OpenAI no es válida o ha expirado. "
                    "Por favor, verifica tu API key en el archivo .env. "
                    "La API key del PDF puede haber expirado. "
                    "Puedes obtener una nueva API key en: https://platform.openai.com/account/api-keys"
                ) from e

            raise

        if not response.choices or len(response.choices) == 0:
            raise ValueError("OpenAI no devolvió ninguna respuesta")

        message_response = response.choices[0].message

        if message_response.tool_calls:
            tool_calls = message_response.tool_calls
            messages.append(message_response)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                function_response = self._execute_tool_call(
                    user, function_name, function_args
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_response),
                    }
                )

            try:
                final_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )

                if not final_response.choices or len(final_response.choices) == 0:
                    raise ValueError("OpenAI no devolvió ninguna respuesta final")

                content = final_response.choices[0].message.content
                if not content:
                    return "Lo siento, no pude generar una respuesta. Por favor, intenta de nuevo."
                return content
            except Exception as e:
                logger.error(f"Error al obtener respuesta final: {str(e)}")
                raise
        else:
            content = message_response.content
            if not content:
                return "Lo siento, no pude generar una respuesta. Por favor, intenta de nuevo."
            return content
