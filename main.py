from fastapi import FastAPI, HTTPException, Request
from utils.get_type_message import get_message_type

app = FastAPI()

# ============================================================
# CONFIGURACIÓN
# ============================================================

# 🔑 ACCESS_TOKEN: Se usa para TODO
ACCESS_TOKEN = "EAAPrCUjHBWYBPwPlmMKZBlCio386SlWewHJtjDoehs1exMVwQpcN8lzPJuwFSmhZAgRVCPPCd8k3DQCCDHbMQvy9oXn37HEkO6nOoBivqFF8uOYZAiOnLak807DmVzGkdwwyf90fIZC2sgESjmJpvseVydb00erBZAvDo5kpFqgwdypLg1hZAWZBdj2FBgxGAZDZD"

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def root():
    """
    ⚠️ ESTE ENDPOINT ES OBLIGATORIO
    Sin él, todas las peticiones dan 404
    """
    return {
        "status": "online",
        "message": "Bot de WhatsApp funcionando correctamente ✅",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Página principal",
            "GET /welcome": "Bienvenida alternativa",
            "GET /whatsapp": "Verificación del webhook",
            "POST /whatsapp": "Recepción de mensajes"
        }
    }


@app.get("/welcome")
def index():
    """Endpoint alternativo de bienvenida"""
    return {"mensaje": "welcome developer"}


@app.get("/whatsapp")
async def verify_token(request: Request):
    """
    Verificación del webhook usando ACCESS_TOKEN.
    
    ⚠️ EN META FOR DEVELOPERS:
    Cuando configures el webhook, en el campo "Verify Token"
    pega tu ACCESS_TOKEN completo.
    """
    try:
        # Obtener los parámetros que Meta envía
        query_params = request.query_params
        
        verify_token = query_params.get("hub.verify_token")
        challenge = query_params.get("hub.challenge")
        mode = query_params.get("hub.mode")
        
        # Logging para debugging
        print("\n" + "=" * 60)
        print("🔍 VERIFICACIÓN DE WEBHOOK")
        print("=" * 60)
        print(f"Mode: {mode}")
        print(f"Challenge: {challenge}")
        
        # Solo mostrar los primeros 30 caracteres del token por seguridad
        if verify_token:
            print(f"Token recibido: {verify_token[:30]}...")
            print(f"Token esperado: {ACCESS_TOKEN[:30]}...")
            print(f"¿Coinciden?: {verify_token == ACCESS_TOKEN}")
        else:
            print("Token recibido: None")
        
        print("=" * 60 + "\n")
        
        # Validación
        if not verify_token or not challenge:
            print("❌ Faltan parámetros")
            raise HTTPException(
                status_code=400,
                detail="Faltan parámetros: hub.verify_token y hub.challenge son requeridos"
            )
        
        # Comparar el token con ACCESS_TOKEN
        if verify_token == ACCESS_TOKEN:
            print("✅ Token verificado correctamente")
            print(f"📤 Devolviendo challenge: {challenge}\n")
            # Devolver el challenge como entero
            return int(challenge)
        else:
            print("❌ Token de verificación inválido")
            raise HTTPException(
                status_code=403,
                detail="Token de verificación inválido"
            )
    
    except HTTPException:
        raise
    
    except ValueError as e:
        # Error al convertir challenge a int
        print(f"❌ Error: challenge no es un número válido: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Challenge inválido: {e}"
        )
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@app.post("/whatsapp")
async def received_message(request: Request):
    """
    Recibe TODOS los mensajes de WhatsApp.
    """
    try:
        # Leer el body
        body = await request.json()
        
        # Verificar estructura básica
        if "entry" not in body:
            print("⚠️ Webhook sin 'entry'")
            return "EVENT_RECEIVED"
        
        entry = body.get("entry", [])
        if not entry:
            return "EVENT_RECEIVED"
        
        changes = entry[0].get("changes", [])
        if not changes:
            return "EVENT_RECEIVED"
        
        value = changes[0].get("value", {})
        
        # Verificar si hay mensajes
        if "messages" in value and len(value["messages"]) > 0:
            message = value["messages"][0]
            
            # Extraer información del mensaje
            type_message, content = get_message_type(message)
            number = message.get("from")
            message_id = message.get("id")
            
            # Logging
            print("\n" + "=" * 60)
            print("📱 MENSAJE RECIBIDO")
            print("=" * 60)
            print(f"De: {number}")
            print(f"ID: {message_id}")
            print(f"Tipo: {type_message}")
            print(f"Contenido: {content}")
            print("=" * 60 + "\n")
            
            # AQUÍ PUEDES AGREGAR TU LÓGICA
            # Ejemplo:
            # bot.process_message(number, type_message, content)
        else:
            # Webhook de estado (mensaje entregado, leído, etc.)
            print("ℹ️ Webhook de estado recibido (no es un mensaje nuevo)")
        
        # SIEMPRE retornar esto
        return "EVENT_RECEIVED"
    
    except KeyError as e:
        print(f"❌ Error de estructura JSON: Falta clave {e}")
        return "EVENT_RECEIVED"
    
    except Exception as e:
        print(f"❌ Error al procesar mensaje: {e}")
        import traceback
        traceback.print_exc()
        return "EVENT_RECEIVED"


# ============================================================
# HEALTH CHECK (Útil para Render)
# ============================================================

@app.get("/health")
def health_check():
    """
    Endpoint para verificar que el servidor está vivo.
    Render usa esto para saber si tu app está funcionando.
    """
    return {
        "status": "healthy",
        "service": "WhatsApp Bot",
        "version": "1.0.0"
    }


# ============================================================
# EJECUTAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("🤖 INICIANDO BOT DE WHATSAPP")
    print("=" * 60)
    print(f"✅ ACCESS_TOKEN configurado")
    print(f"📝 Primeros 30 caracteres: {ACCESS_TOKEN[:30]}...")
    print("=" * 60)
    print("🌐 Servidor: http://0.0.0.0:8000")
    print("📚 Documentación automática: http://0.0.0.0:8000/docs")
    print("=" * 60)
    print("\n⚠️  IMPORTANTE para Meta for Developers:")
    print("   Callback URL: https://tu-dominio.onrender.com/whatsapp")
    print("   Verify Token: [Pega tu ACCESS_TOKEN completo]")
    print("=" * 60 + "\n")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)