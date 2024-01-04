#Copyright ©️ 2022 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [Ping All Telegram bot by TeLe TiPs] (https://github.com/etmusict/taggalls)

# Changing the code is not allowed! Read GNU AFFERO GENERAL PUBLIC LICENSE: https://github.com/etmusict/taggalls/blob/main/LICENSE

from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

teletips=Client(
    "PingAllBot",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

chatQueue = []

stopProcess = False

@teletips.on_message(filters.command(["ping","all","@all","تاك","تاك للكل"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 5:
        await message.reply("⛔️ | أنا أعمل بالفعل على الحد الأقصى لعدد الدردشات وهو 5 في الوقت الحالي. يرجى المحاولة مرة أخرى بعد قليل.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 | هناك بالفعل عملية جارية في هذه المجموعه. من فضلك اوقف القديمه وشغل واحدة جديدة.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.command[1]
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in teletips.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await teletips.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(10) 
              i+=10
            except IndexError:
              try:
                await teletips.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅ | تم عمل التاك **عدد الاعضاء {i} **.") 
          else:
            await message.reply(f"✅ | تم بلفعل عمل تاك الي **{i} في المجموعه.**")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | اسف** يمكن للمشرفين فقط**تنفيذ هذا الأمر.")  
  except FloodWait as e:
    await asyncio.sleep(e.value) 

@teletips.on_message(filters.command(["remove","clean","حذف الحسابات","حذف الحسبات"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await teletips.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 | أحتاج اذن الحظر لإزالة الحسابات المحذوفة.")  
      else:  
        if len(chatQueue) > 5 :
          await message.reply("⛔️ | أنا أعمل بالفعل على الحد الأقصى لعدد الدردشات وهو 5 في الوقت الحالي. يرجى المحاولة مرة أخرى بعد قليل.")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 | هناك بالفعل عملية جارية في هذه المجموعه. من فضلك اوقف القديمه وشغل واحدة جديدة.")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in teletips.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 | لا توجد حسابات محذوفة في هذه المجموعه.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await teletips.send_message(message.chat.id, f"🚨 | مجموع {lenDeletedList} الحسابات المحذوفة.\n⏳ | الوقت المستغرق: {processTime} ثواني من الان.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await teletips.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅ | تمت إزالة جميع الحسابات المحذوفة من هذه الدردشة بنجاح.")  
                await temp.delete()
              else:
                await message.reply(f"✅ | تمت الإزالة بنجاح {k} من الحسابات المحذوفة من هذه المجموعه.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | اسف** يمكن للمشرفين فقط**تنفيذ هذا الأمر.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        
@teletips.on_message(filters.command(["stop","cancel","ايقاف","ايقاف التاك","ايقاف تاك"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | لا توجد عملية جارية لإيقافها.")
      else:
        stopProcess = True
        await message.reply("🛑 | تم الايقاف بنجاح.")
    else:
      await message.reply("👮🏻 | اسف** يمكن للمشرفين فقط**تنفيذ هذا الأمر..")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command(["admins","staff","الادمنيه","الادمنية","المالك"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**طاقم المجموعه - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 **مالك المجموعه** \n└ {owner.mention}\n\n👮🏻 **الادمنيه** \n"
      else:
        text2 += f"👑 **مالك المجموعه** \n└ @{owner.username}\n\n👮🏻 **الادمنيه** \n"
    except:
      text2 += f"👑 **مالك المجموعه** \n└ <i>Hidden</i>\n\n👮🏻 **الادمنيه** \n"
    if len(adminList) == 0:
      text2 += "└ <i>Admins are hidden</i>"  
      await teletips.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **العدد الإجمالي للمسؤولين**: {lenAdminList} ."  
      await teletips.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@teletips.on_message(filters.command("bots","البوتات","بوتات الجروب"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"<i>**بوتات الجروب 🤖**</i>- {message.chat.title} \n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | <i>**العدد الإجمالي للبوتات**</i> : {lenBotList}"  
      await teletips.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command("start","تفعيل") & filters.private)
async def start(client, message):
  text = f'''
<i>**مرحبا عزيزي المستخدم** {message.from_user.mention},</i> 💞.\n **في بوت التاك الأفضل والاسرع في التليجرام🚀** \n **البوت مزود بعدد اوامر اضافيه غير موجوده في بوتات التليجرام وهذا هو المميز في هذا البوت🚧** \n **لعرض اوامر البوت الرجاء ارسال الامر** /help **وانظر الاوامر وطريقه عمل البوت🗽** .
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)


@teletips.on_message(filters.command("help","المساعده","الاعدادات","الأعدادات"))
async def help(client, message):
  text = '''
**اوامر البوت ايضا متواجده في الجروب**.

**الاوامر**:
- /ping @all : <i>لعمل تاك للمجموعه.</i>
- /remove حذف الحسابات : <i>حذف الحسابات المحذوفه.</i>
- /admins الادمنيه : <i>ادمنيه المجموعه.</i>
- /bots بوتات : <i>بوتات الجروب.</i>
- /stop ايقاف التاك : <i>ايقاف التاك.</i>
.
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)

print("PingAll is alive!")  
teletips.run()
 
#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved 
