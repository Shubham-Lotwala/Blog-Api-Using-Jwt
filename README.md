
# Blog Api Using Jwt

This project provides a user authentication system using Django and Django REST Framework. It includes features such as user registration, login, password change, and password reset etc

## In this Blog Api, I have used a security measure so that no one can edit or delete any other post except their own.

## Installation

- Clone the repository 
- Apply the migrations
- Create a superuser
- Run the development server

## Usage 

- User Registration
`[POST] /api/register/`
- User Login
`[POST] /api/login/`
- Get Post
 `[GET] /api/blogs/`
- Forgot Password
 `[POST] /api/forgot-password/`
- Send Password Reset Email
 `[POST] /api/reset-password/<token>`
- Update Post
 `[PUT] /api/blogs/<id>/`
- Delete Post
`[DELETE] /api/blogs/<id>/` 
 
## Email Configuration

To send password reset emails, you need to configure your email settings in the `settings.py` file. Make sure to set the `EMAIL_FROM` environment variable with your email address.

- EMAIL_BACKEND  
`'django.core.mail.backends.smtp.EmailBackend'`
- EMAIL_HOST  
`'smtp.your-email-provider.com'`
- EMAIL_PORT  
`587`
- EMAIL_USE_TLS  
`True`
- EMAIL_HOST_USER  
`'your-email@example.com'`
- EMAIL_HOST_PASSWORD  
`'your-email-password'`



## Register 

![Home Pages1](https://github.com/Shubh556/Django_Rest_Auth/blob/main/img/register.png?raw=true)

## Login 
![Home Pages1](https://github.com/Shubh556/Django_Rest_Auth/blob/main/img/Login.png?raw=true)


## Get Post
![Home Pages1](https://github.com/Shubham-Lotwala/Blog-Api-Using-Jwt/blob/main/blogapi/Img/get.png?raw=true)

## Add Post in Database

![Home Pages1](https://github.com/Shubham-Lotwala/Blog-Api-Using-Jwt/blob/main/blogapi/Img/send%20post%20to%20server.png?raw=true)

## Update Post

![Home Pages1](https://github.com/Shubham-Lotwala/Blog-Api-Using-Jwt/blob/main/blogapi/Img/Update%20Post.png?raw=true)

## Delete Post 

![Home Pages1](https://github.com/Shubham-Lotwala/Blog-Api-Using-Jwt/blob/main/blogapi/Img/Delete%20Post.png?raw=true)

## Send Reset Email

![Home Pages1](https://github.com/Shubh556/Django_Rest_Auth/blob/main/img/send%20reset%20email.png?raw=true)

## Reset Email Token 
![Home Pages1](https://github.com/Shubh556/Django_Rest_Auth/blob/main/img/reset%20email%20token.png?raw=true)

## Password Reset Successfull
![Home Pages1](https://github.com/Shubh556/Django_Rest_Auth/blob/main/img/successfull%20password%20reset%20.png?raw=true)




