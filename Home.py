class User:
    def __init__(self, username, password, fingerprint_id, face_image_path):
        self.username = username
        self.password = password
        self.fingerprint_id = fingerprint_id
        self.face_image_path = face_image_path
        self.logged_in = False

    def login(self, username, password):
        if username == self.username and password == self.password:
            self.logged_in = True
            print("登录成功！")
        else:
            print("用户名或密码错误！")

    def logout(self):
        self.logged_in = False
        print("已登出。")

    def voice(self):
        print("这是一个普通用户的函数，所有用户都可以调用。")

    def register(self):
        user_info = f"{self.username},{self.password},{type(self).__name__}"
        with open('users.txt', 'a') as file:
            file.write(user_info + '\n')
        print("注册成功！")


class FamilyUser(User):
    def __init__(self, username, password, fingerprint_id, face_image_path):
        super().__init__(username, password, fingerprint_id, face_image_path)
        self.permissions = ['read', 'write', 'delete']

    def voice(self):
        print("这是一个FamilyUser特有的函数，只有FamilyUser可以调用。")


class GuestUser(User):
    def __init__(self, username, password, fingerprint_id, face_image_path):
        super().__init__(username, password, fingerprint_id, face_image_path)
        self.permissions = ['read']

    def voice(self):
        print("这是一个GuestUser特有的函数，只有GuestUser可以调用。")


class AdminUser(User):
    def __init__(self, username, password, fingerprint_id, face_image_path):
        super().__init__(username, password, fingerprint_id, face_image_path)
        self.permissions = ['read', 'write', 'delete', 'manage_users']

    def add_user(self, user):
        # 实现添加用户的逻辑
        pass


# 创建用户对象示例
family_user = FamilyUser('john', 'password123', 'fingerprint_123', '/path/to/face_image.jpg')
guest_user = GuestUser('guest1', 'guestpass', 'fingerprint_456', '/path/to/face_image.jpg')

# 注册示例
family_user.register()
guest_user.register()
