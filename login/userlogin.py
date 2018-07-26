from lib.User import  User
import lib.item_object


def UserLogin(get_user,get_pass):
    '''用户登录'''
    #注册用户类
    user = User(get_user)
    # 检查用户是否注册
    if user.getUserID() == None:
        return "账号未注册，请注册"
    # 验证用户密码
    print(get_user,get_pass)
    if user.getUserPasswd() == get_pass:
        user.uploadUserinfo()
        # 如果登录成功返回user对象
        return user()
    else:
        raise ValueError("密码错误")



if __name__ == '__main__':
    UserLogin()
