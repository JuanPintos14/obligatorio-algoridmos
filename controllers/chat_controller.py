from services.whatsapp_service import WhatsAppService
from typing import Dict, Callable, Any

whatsapp = WhatsAppService()

# Enviar un mensaje simple
whatsapp.send_text_message(
    phone_number="59892717261",
    text="¡Hola! Tu pedido está listo 🍕"
)
class ChatController:
    """Controlador principal del bot"""
    
    def __init__(self):
        self.whatsapp = WhatsAppService()
        
        # Almacena el estado de cada usuario por su número de teléfono
        # Estructura: {phone_number: {waiting_for: función, data: {}}}
        self.user_states: Dict[str, Dict[str, Any]] = {}
    
    def get_user_state(self, phone_number: str) -> Dict[str, Any]:
        """Obtiene o crea el estado de un usuario"""
        if phone_number not in self.user_states:
            self.user_states[phone_number] = {
                "waiting_for": None,
                "data": {}
            }
        return self.user_states[phone_number]
    
    def set_waiting_for(self, phone_number: str, function: Callable):
        """Define qué función debe manejar la próxima respuesta del usuario"""
        state = self.get_user_state(phone_number)
        state["waiting_for"] = function
    
    def process_message(self, phone_number: str, message_type: str, content: Any):
        """
        Procesa un mensaje entrante.
        Este es el PUNTO DE ENTRADA principal.
        """
        state = self.get_user_state(phone_number)
        
        # Si el usuario está esperando una respuesta específica
        if state["waiting_for"]:
            waiting_func = state["waiting_for"]
            waiting_func(phone_number, message_type, content)
        
        # Si es un mensaje nuevo o un comando
        elif message_type == "text":
            text = content.lower().strip()
            
            if text in ["/start", "/iniciar", "hola", "menu"]:
                self.show_welcome_menu(phone_number)
            else:
                # Si no entiende el mensaje, mostrar ayuda
                self.whatsapp.send_text_message(
                    phone_number,
                    "❌ No entendí tu mensaje.\n\nEscribe /start para ver el menú."
                )
    
    # ============================================================
    # FUNCIONES DE CONVERSACIÓN
    # ============================================================
    
    def show_welcome_menu(self, phone_number: str):
        """Muestra el menú principal"""
        buttons = [
            {"id": "ver_productos", "title": "🍕 Ver Productos"},
            {"id": "mi_carrito", "title": "🛒 Mi Carrito"},
            {"id": "mis_pedidos", "title": "📦 Mis Pedidos"}
        ]
        
        self.whatsapp.send_button_message(
            phone_number,
            "🤖 ¡Bienvenido a nuestro Restaurante!\n\n¿Qué deseas hacer?",
            buttons
        )
        
        # Esperamos que el usuario presione un botón
        self.set_waiting_for(phone_number, self.handle_menu_selection)
    
    def handle_menu_selection(self, phone_number: str, message_type: str, content: Any):
        """Maneja la selección del menú principal"""
        
        if message_type != "interactive":
            self.whatsapp.send_text_message(
                phone_number,
                "❌ Por favor, selecciona una opción del menú."
            )
            self.show_welcome_menu(phone_number)
            return
        
        button_id = content
        
        if button_id == "ver_productos":
            self.show_products_list(phone_number)
        
        elif button_id == "mi_carrito":
            self.show_cart(phone_number)
        
        elif button_id == "mis_pedidos":
            self.show_orders(phone_number)
    
    def show_products_list(self, phone_number: str):
        """Muestra la lista de productos"""
        
        # AQUÍ debes cargar tus 25 productos desde tu base de datos
        # Por ahora, ejemplo con datos mock:
        
        products = [
            {"id": "prod_1", "name": "Pizza Napolitana", "price": 450, "category": "Pizzas"},
            {"id": "prod_2", "name": "Hamburguesa Completa", "price": 380, "category": "Minutas"},
            {"id": "prod_3", "name": "Coca-Cola 1.5L", "price": 120, "category": "Bebidas"},
            {"id": "prod_4", "name": "Milanesa con Papas", "price": 420, "category": "Minutas"},
            {"id": "prod_5", "name": "Pizza Muzzarella", "price": 400, "category": "Pizzas"},
        ]
        
        # Crear secciones para la lista
        sections = [
            {
                "title": "Productos Disponibles",
                "rows": [
                    {
                        "id": p["id"],
                        "title": p["name"],
                        "description": f"${p['price']} - {p['category']}"
                    }
                    for p in products[:5]  # Mostrar solo 5 por página
                ]
            }
        ]
        
        self.whatsapp.send_list_message(
            phone_number,
            "🍽️ Selecciona un producto:",
            "Ver Productos",
            sections
        )
        
        self.set_waiting_for(phone_number, self.handle_product_selection)
    
    def handle_product_selection(self, phone_number: str, message_type: str, content: Any):
        """Maneja cuando el usuario selecciona un producto"""
        
        if message_type != "interactive":
            self.whatsapp.send_text_message(
                phone_number,
                "❌ Por favor, selecciona un producto de la lista."
            )
            self.show_products_list(phone_number)
            return
        
        product_id = content
        
        # Aquí buscarías el producto en tu base de datos
        # Por ahora, simulamos:
        product_name = "Pizza Napolitana"  # Buscar por product_id
        
        self.whatsapp.send_text_message(
            phone_number,
            f"✅ Seleccionaste: {product_name}\n\n¿Cuántas unidades deseas?"
        )
        
        # Guardamos el producto seleccionado en el estado del usuario
        state = self.get_user_state(phone_number)
        state["data"]["selected_product"] = product_id
        
        self.set_waiting_for(phone_number, self.handle_quantity_input)
    
    def handle_quantity_input(self, phone_number: str, message_type: str, content: Any):
        """Maneja cuando el usuario ingresa la cantidad"""
        
        if message_type != "text":
            self.whatsapp.send_text_message(
                phone_number,
                "❌ Por favor, envía la cantidad como un número (ej: 2)"
            )
            return
        
        try:
            quantity = int(content)
            if quantity <= 0:
                raise ValueError
            
            # Guardar cantidad en el estado
            state = self.get_user_state(phone_number)
            state["data"]["quantity"] = quantity
            
            self.whatsapp.send_text_message(
                phone_number,
                f"✅ Cantidad: {quantity}\n\n¿Alguna aclaración? (ej: 'Sin tomate')\n\nResponde NO si no tienes aclaraciones."
            )
            
            self.set_waiting_for(phone_number, self.handle_product_details)
        
        except ValueError:
            self.whatsapp.send_text_message(
                phone_number,
                "❌ Cantidad inválida. Por favor, envía un número mayor a 0."
            )
    
    def handle_product_details(self, phone_number: str, message_type: str, content: Any):
        """Maneja las aclaraciones del producto"""
        
        state = self.get_user_state(phone_number)
        
        if message_type == "text" and content.lower() != "no":
            state["data"]["details"] = content
        else:
            state["data"]["details"] = "Sin aclaraciones"
        
        # AQUÍ deberías agregar el producto al carrito
        # Por ahora solo confirmamos:
        
        self.whatsapp.send_text_message(
            phone_number,
            f"✅ Producto agregado al carrito!\n\n"
            f"Producto: {state['data']['selected_product']}\n"
            f"Cantidad: {state['data']['quantity']}\n"
            f"Aclaraciones: {state['data']['details']}\n\n"
            f"¿Qué deseas hacer ahora?"
        )
        
        # Limpiar datos temporales
        state["data"] = {}
        
        # Volver al menú principal
        self.show_welcome_menu(phone_number)
    
    def show_cart(self, phone_number: str):
        """Muestra el carrito del usuario"""
        # IMPLEMENTAR: Mostrar productos en el carrito
        self.whatsapp.send_text_message(
            phone_number,
            "🛒 Tu carrito está vacío.\n\nEscribe /start para ver productos."
        )
    
    def show_orders(self, phone_number: str):
        """Muestra los pedidos del usuario"""
        # IMPLEMENTAR: Mostrar historial de pedidos
        self.whatsapp.send_text_message(
            phone_number,
            "📦 No tienes pedidos aún.\n\nEscribe /start para hacer un pedido."
        )