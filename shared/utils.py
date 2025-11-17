def get_message_type(message):
    """
    Extrae el tipo y contenido de un mensaje de WhatsApp.
    
    Tipos posibles:
    - text: mensaje de texto simple
    - interactive: botón o lista
    - image: imagen
    - audio: nota de voz
    - location: ubicación
    """
    content = ""
    message_type = message.get("type", "unknown")

    if message_type == "text":
        content = message["text"]["body"]
    
    elif message_type == "interactive":
        interactive_object = message["interactive"]
        interactive_type = interactive_object["type"]

        if interactive_type == "button_reply":
            content = interactive_object["button_reply"]["id"]  # ¡IMPORTANTE: usa 'id' no 'title'!
        elif interactive_type == "list_reply":
            content = interactive_object["list_reply"]["id"]  # ¡IMPORTANTE: usa 'id' no 'title'!
    
    elif message_type == "location":
        content = message["location"]  # Devuelve el objeto completo con lat/lon
    
    elif message_type == "audio":
        content = message["audio"]["id"]  # ID del audio para descargarlo
    
    else:
        content = None

    return message_type, content