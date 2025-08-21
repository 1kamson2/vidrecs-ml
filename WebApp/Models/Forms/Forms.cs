namespace WebApp.Models.Forms;

using Microsoft.AspNetCore.Mvc;
using WebApp.Interfaces;
using System.Text.Json;

public class LoginForm : IDeserialization<LoginForm>
{
    public String Username { get; set; }
    public String Password { get; set; }

    public LoginForm(
            String username,
            String password
            )
    {
        Username = username;
        Password = password;
    }

    public static LoginForm FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("username", out JsonElement username))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("password", out JsonElement password))
        {
            Console.WriteLine("do sth");
        }
        return new LoginForm(
                username.GetString(),
                password.GetString()
                );
    }
}

public class RegisterForm : IDeserialization<RegisterForm>
{
    public String Email { get; set; }
    public String Username { get; set; }
    public String Password { get; set; }
    public Int16 Age { get; set; }

    private RegisterForm(
            String email,
            String username,
            String password,
            Int16 age
            )
    {
        Email = email;
        Username = username;
        Password = password;
        Age = age;
    }

    public static RegisterForm FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("email", out JsonElement email))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("username", out JsonElement username))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("password", out JsonElement password))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("age", out JsonElement age))
        {
            Console.WriteLine("do sth");
        }

        return new RegisterForm(
                email.GetString(),
                username.GetString(),
                password.GetString(),
                age.GetInt16()
                );
    }
}

public class GameForm : IDeserialization<GameForm>
{
    private String _token;
    private String _request;
    public String Token { get => _token; }
    public String Request { get => _request; }

    private GameForm(
            String token,
            String request
            )
    {
        _request = request;
        _token = token;
    }

    public static GameForm FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("token", out JsonElement token))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("request", out JsonElement request))
        {
            Console.WriteLine("do sth");
        }

        return new GameForm(
                token.GetString(),
                request.GetString()
                );
    }
}
