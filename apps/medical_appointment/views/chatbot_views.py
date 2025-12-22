import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..services import ChatbotService

logger = logging.getLogger(__name__)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot_service = ChatbotService()

    def post(self, request):
        """Endpoint para interactuar con el chatbot"""
        message = request.data.get("message")
        conversation_history = request.data.get("conversation_history", [])

        if not message:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = self.chatbot_service.get_response(
                request.user, message, conversation_history
            )
            return Response({"response": response}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Error de validación en chatbot: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error en chatbot: {error_message}", exc_info=True)

            if "401" in error_message or "invalid_api_key" in error_message.lower():
                user_message = "La API key de OpenAI no es válida. Por favor, verifica la configuración en el archivo .env"
            elif "429" in error_message or "rate_limit" in error_message.lower():
                user_message = "Se ha excedido el límite de solicitudes a OpenAI. Por favor, intenta más tarde."
            elif "500" in error_message or "internal" in error_message.lower():
                user_message = "Error interno en el servicio de OpenAI. Por favor, intenta más tarde."
            else:
                user_message = f"Error al procesar la solicitud: {error_message}"

            return Response(
                {"error": user_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
