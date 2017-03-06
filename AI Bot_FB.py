import fbchat
import getpass

username="xentrous@gmail.com"

password=getpass.getpass("Enter Password:")

client = fbchat.Client(username, password)

client.listen(client)
