namespace WebApp.Models.Requests;
using System.Text.Json;
using WebApp.Interfaces;
using WebApp.Models.Forms;

public class RegisterRequest : ApiMessage<RegisterForm>, IDeserialization<RegisterRequest>
{
    public RegisterRequest(
            String sender,
            String receiver,
            RegisterForm content
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

    public static RegisterRequest FromJson(JsonElement json)
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

        RegisterForm form = RegisterForm.FromJson(content);

        return new RegisterRequest(
                sender.GetString(),
                receiver.GetString(),
                form
                );
    }
}
