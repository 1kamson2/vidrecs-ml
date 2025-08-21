namespace WebApp.Models.Requests;
using System.Text.Json;
using WebApp.Interfaces;
using WebApp.Models.Forms;

public class LoginRequest : ApiMessage<LoginForm>, IDeserialization<LoginRequest>, ISerialization<LoginRequest>
{
    private LoginRequest(
            String sender,
            String receiver,
            LoginForm content
            ) : base(sender, receiver, content)
    { }

    public StringContent ToJson()
    {
        return new StringContent(
                JsonSerializer.Serialize(this,
                    new JsonSerializerOptions
                    {
                        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                    }
                    ),
                System.Text.Encoding.UTF8,
                "application/json"
                );
    }

    public static LoginRequest FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("sender", out JsonElement sender))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("receiver", out JsonElement receiver))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("content", out JsonElement content))
        {
            Console.WriteLine("do sth");
        }

        LoginForm form = LoginForm.FromJson(content);

        return new LoginRequest(
                sender.GetString(),
                receiver.GetString(),
                form
                );
    }
}
