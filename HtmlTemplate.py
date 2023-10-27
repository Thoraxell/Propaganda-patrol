css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 0%;
}
.chat-message .avatar img {
  max-width: 1px;
  max-height: 1px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 100%;
  padding: 0 0.5rem;
  color: #fff;
}
 
.st-emotion-cache {
  border: 1px;
  border-color: red;
}
'''
 
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <!-- Image removed from here -->
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
 
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <!-- Image removed from here -->
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
