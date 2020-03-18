from django.shortcuts import render

# Create your views here.
from apps.webs.models import Message

#get 拉  post推
def message_form(request):
    # all_messages = Message.objects.filter(name="bobby") #all_messages.query
    # for message in all_messages:
    #     print(message.name)

    #get 返回一个对象， 数据不存在会抛出异常
    # try:
    #  message = Message.objects.get(name="bobby1")
    # except Message.DoesNotExist as e:
    #     pass
    # except Message.MultipleObjectsReturned as e:
    #     pass
    #删除 message.delete()
    #插入数据

    # message.name = "bobby"
    # message.email = "ls"
    # message.address = "北京"
    # message.message = "更新"
    #
    # message.save() #如果存在则更新，如果不存在则插入

 #  提取数据并保存

    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        address = request.POST.get("address","")
        message_text = request.POST.get("message","")
        message = Message()
        message.name = name
        message.email = email
        message.address = address
        message.message = message_text
        message.save()
        return render(request, "message_form.html", {
            "message":message
        })
    if request.method == "GET":
        var_dict = {}
        all_message = Message.objects.all()
        if all_message:
            message = all_message[0]
            var_dict = {
                "message":message
            }
            print(message.message)

        return render(request,"message_form.html",var_dict)
