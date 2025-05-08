from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
import requests
import logging
import re
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('BOT_API')
#Mostrar los log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




async def keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            logger.warning("El mensaje no está disponible.")
            return

        message_text = update.message.text.replace("/keyword", "").strip()

        #  extraer parametros clave=valor
        params = re.findall(r"(\w+)=(\"[^\"]+\"|\S+)", message_text)

        # Convertir a un diccionario
        data = {key: value.strip('\"') for key, value in params}

        keyword_content = data.get("keyword", None)
        porcentage = int(data.get("porcentage", 0)) 
        max_page = int(data.get("max_page", 1))  
        store_id = int(data.get("store_id", 0))  
        active = bool(int(data.get("active", 1)))  
        alert_new = bool(int(data.get("alert_new", 0)))  
        category = data.get("category", None)
        blacklist = data.get("blacklist", None)
        sort = data.get("sort", None)
        landing_url = data.get("landing_url", None)

        if not keyword_content:
            await update.message.reply_text("Error: El parámetro 'keyword' es obligatorio.")
            return

        payload = {
            "keyword": keyword_content,
            "porcentage": porcentage,
            "max_page": max_page,
            "store_id": store_id,
            "active": active,
            "alert_new": alert_new,
            "category": category,
            "blacklist": blacklist,
            "sort": sort,
            "landing_url": landing_url
        }

        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTYyNjc3ODAwMX0.AEgTfrLQ4jSiz7mnIZObimW0BDSVDjkaCbbvzp5vfAk'

        url = 'http://localhost:8001/keyword/add'

        headers = {
            'Authorization': f'Bearer {token}'  
        }

        response = requests.post(url, json=payload, headers=headers)

        # Responde en el canal
        if response.status_code == 200:
            await update.message.reply_text(f"🎉 *Keyword añadida correctamente* ✅",parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Hubo un error al añadir el keyword: {response.text}")

    except IndexError:
        await update.message.reply_text("Error: El comando no tiene suficientes argumentos.")
    except ValueError:
        await update.message.reply_text("Error: Asegúrate de que los valores sean correctos.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text(f"Error inesperado: {e}")

# UPDATE 
async def update_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            logger.warning("El mensaje no está disponible.")
            return

        message_text = update.message.text.replace("/update", "").strip()

        params = re.findall(r"(\w+)=(\"[^\"]+\"|\S+)", message_text)

        data = {key: value.strip('\"') for key, value in params}

        if "id" not in data:
            await update.message.reply_text("Error: El parámetro 'id' es obligatorio.")
            return
        
        keyword_id = int(data["id"])

        keyword_content = data.get("keyword", None)
        porcentage = int(data.get("porcentage", 0))
        max_page = int(data.get("max_page", 1))
        store_id = int(data.get("store_id", 0))
        active = bool(int(data.get("active", 1)))
        alert_new = bool(int(data.get("alert_new", 0)))
        category = data.get("category", None)
        blacklist = data.get("blacklist", None)
        sort = data.get("sort", None)
        landing_url = data.get("landing_url", None)

        payload = {
            "porcentage": porcentage,
            "keyword": keyword_content,
            "max_page": max_page,
            "store_id": store_id,
            "active": active,
            "alert_new": alert_new,
            "category": category,
            "blacklist": blacklist,
            "sort": sort,
            "landing_url": landing_url
        }

        url = f'http://localhost:8001/keyword/update/{keyword_id}'

        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTYyNjc3ODAwMX0.AEgTfrLQ4jSiz7mnIZObimW0BDSVDjkaCbbvzp5vfAk'

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.put(url, json=payload, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text(f"🎉 *Keyword con ID: {keyword_id} actualizada correctamente* ✅",parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Hubo un error al actualizar la keyword: {response.text}")

    except IndexError:
        await update.message.reply_text("Error: El comando no tiene suficientes argumentos.")
    except ValueError:
        await update.message.reply_text("Error: Asegúrate de que los valores sean correctos.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text(f"Error inesperado: {e}")
# DELETE 
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            logger.warning("El mensaje no está disponible.")
            return

        keyword_id = int(context.args[0])

        url = f'http://localhost:8001/keyword/delete/{keyword_id}'

        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTYyNjc3ODAwMX0.AEgTfrLQ4jSiz7mnIZObimW0BDSVDjkaCbbvzp5vfAk'  

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text(f"*Keyword con ID: {keyword_id} Borrada correctamente* ✅",parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Hubo un error al eliminar el keyword: {response.text}")

    except IndexError:
        await update.message.reply_text("Error: El comando no tiene suficientes argumentos.")
    except ValueError:
        await update.message.reply_text("Error: Asegúrate de que el ID sea un número válido.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text(f"Error inesperado: {e}")
# VIEW
async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            logger.warning("El mensaje no está disponible.")
            return

        keyword_id = int(context.args[0])

        url = f'http://localhost:8001/keyword/{keyword_id}'

        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTYyNjc3ODAwMX0.AEgTfrLQ4jSiz7mnIZObimW0BDSVDjkaCbbvzp5vfAk'  

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            keyword_data = response.json()
            print(f'keyword_data {keyword_data}')
            keyword = keyword_data['keyword']
            active = keyword['active']
            if active == True:
                active = '1'
            elif active == False:
                active = '0'
            else:
                active = active
            alert_new = keyword['alert_new']
            if alert_new == True:
                alert_new = '1'
            elif alert_new == False:
                alert_new = '0'
            else:
                alert_new = 'llega aca'
            message = (
                f"🔍 *Detalles del Keyword:* \n\n"
                f"*ID:* `{keyword['id']}`\n\n"
                f"*Keyword:* `{keyword['keyword']}`\n\n"
                f"*Porcentage:* `{keyword['porcentage']}%`\n\n"
                f"*Max Page:* `{keyword['max_page']}`\n\n"
                f"*Store ID:* `{keyword['store_id']}`\n\n"
                f"*Activate:* `{keyword['active']}`\n\n"
                f"*Alert New:* `{keyword['alert_new']}`\n\n"
                f"*Comando para actualizar* \n"
                f"/update id={keyword['id']}\n"
                f"keyword=\"{keyword['keyword']}\" \n"
                f"porcentage={keyword['porcentage']} \n"
                f"max\\_page={keyword['max_page']} \n"
                f"store\\_id={keyword['store_id']} \n"
                f"active={active} \n"
                f"alert\\_new={alert_new} \n"
            )
            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Hubo un error al obtener el keyword: {response.text}")

    except IndexError:
        await update.message.reply_text("Error: El comando no tiene suficientes argumentos.")
    except ValueError:
        await update.message.reply_text("Error: Asegúrate de que el ID sea un número válido.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text(f"Error inesperado: {e}") 


async def get_keywords_by_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("Por favor, proporciona un store_id.")
            return

        store_id = int(context.args[0])

        base_url = "http://localhost:8001"
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTYyNjc3ODAwMX0.AEgTfrLQ4jSiz7mnIZObimW0BDSVDjkaCbbvzp5vfAk' 

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Obtener el nombre de la tienda
        store_response = requests.get(f"{base_url}/store/{store_id}", headers=headers)
        if store_response.status_code != 200:
            await update.message.reply_text(f"Error al obtener el nombre de la tienda: {store_response.text}")
            return
        
        store_data = store_response.json()
        store_name = store_data["store"]["name"] if "store" in store_data else f"ID {store_id}"

        # Obtener las keywords de la tienda
        keyword_response = requests.get(f"{base_url}/keyword/store/{store_id}", headers=headers)
        if keyword_response.status_code != 200:
            await update.message.reply_text(f"Error al obtener las keywords: {keyword_response.text}")
            return

        keywords_data = keyword_response.json()
        keywords = keywords_data.get('keywords', [])

        if keywords:
            message = f"🛒 *Tienda: {store_name} (ID: {store_id})*\n\n🔍 *Lista de Keywords:*\n\n"
            for keyword in keywords:
                status_emoji = "✅" if keyword['active'] == True else "❌"
                message += f"🎯*ID:* `{keyword['id']}` {status_emoji}\n"
                message += f"🔑 *Keyword:* `{keyword['keyword']}`\n"
                message += "➖➖➖➖➖➖➖➖➖➖\n"  

            max_message_length = 4096
            while len(message) > max_message_length:
                await update.message.reply_text(message[:max_message_length], parse_mode="Markdown")
                message = message[max_message_length:]

            if message:
                await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"No se encontraron keywords para la tienda *{store_name}* (`ID {store_id}`).", parse_mode="Markdown")

    except IndexError:
        await update.message.reply_text("Error: El comando no tiene suficientes argumentos.")
    except ValueError:
        await update.message.reply_text("Error: Asegúrate de que el ID sea un número válido.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        await update.message.reply_text(f"Error inesperado: {e}")

    
# Help
async def help_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌟 *Comandos Disponibles* 🌟\n\n"
        "❗*Si deseas añadir o actualizar keywords con espacios, colócalas entre comillas:*\n"
        "Ejemplo: keyword=\"moviles samsung\"\n\n"
        
        "⚠️ *Si en el chat fijado se indica que se pueden utilizar categorías, debes añadir:*\n"
        " `category=nombreCategoria` en los comandos /add y /update después de `alert_new`.\n\n"
        
        "🚨 *Valores booleanos:*\n"
        "   Los valores `active` y `alert_new` son booleanos, lo que significa que:\n"
        "*- False = 0*\n"
        "*- True = 1*\n\n"
        
        "🔑 *Añadir una nueva keyword /add :*\n"
        "*/add keyword=pc\n"
        "porcentage=10\n"
        "max_page=5\n"
        "store_id=1\n"
        "active=1\n"
        "alert_new=1*\n\n"
        
        "✏️ *Actualizar una keyword existente /update :*\n"
        "*/update id=300\n"
        "keyword=pc\n"
        "porcentage=30\n"
        "max_page=10\n"
        "store_id=45\n"
        "active=1\n"
        "alert_new=1*\n\n"
        
        "🗑️ *Eliminar una keyword /delete :*\n"
        "*/delete 'id'*\n\n"
        
        "🔍 *Ver una keyword por ID /view :*\n"
        "*/view 'id'*\n\n"
        
        "📂 *Ver todas las keywords de una tienda /keywords_store :*\n"
        "*/keywords_store 'id'*"
    )

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text(f"Ha ocurrido un error: {context.error}")


def main():

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("help", help_user))
    application.add_handler(CommandHandler("add", keyword))
    application.add_handler(CommandHandler("update", update_keyword))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("view", view))
    application.add_handler(CommandHandler("keywords_store", get_keywords_by_store))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
