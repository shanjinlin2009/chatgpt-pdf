css = '''
<style>
.chat-message{
    padding:1.5rem;
    border-radius:0.5rem;
    margin-bottom:1rem;
    display:flex;
}
.chat-message.user{
    background-color:#2b313e;
}
.chat-message.bot{
    background-color:#475063;
}
.chat-message .avatar{
    width:15%;
}
.chat-message .avatar img{
    max-width:78px;
    max-height:78px;
    border-radius:50%;
    object-fit:cover;
}
.chat-message .message{
    width:85%;
    padding:0 1.5rem;
    color:#fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://current.vc/current/image/company_logo/2feedf13a4f859b50fefd09327b3d53f.jpg" />
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img2.baidu.com/it/u=3741912865,1157571944&fm=253&fmt=auto&app=138&f=JPEG?w=440&h=385" />
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''