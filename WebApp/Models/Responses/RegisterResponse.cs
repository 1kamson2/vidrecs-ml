namespace WebApp.Models.Responses;

using System.Text.Json;
using WebApp.Interfaces;
using WebApp.Models.Requests;


public sealed class RegisterResponse : ApiMessage<String>, IDeserialization<RegisterResponse>
{
    public RegisterResponse(
            String sender,
            String receiver,
            String token
            ) : base(sender, receiver, token)
    { }

    static public RegisterResponse FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("id", out JsonElement id))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("sender", out JsonElement sender))
        {
            Console.WriteLine("do sth");

        }

        if (!json.TryGetProperty("receiver", out JsonElement receiver))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("content", out JsonElement token))
        {
            Console.WriteLine("do sth");
        }

        return new RegisterResponse(
                sender.GetString(),
                receiver.GetString(),
                token.GetString()
                );
    }

    static public JsonElement? ReadHttpContent(String content)
    {
        // TODO: Add error handling
        var jsonDoc = JsonDocument.Parse(content);
        return jsonDoc.RootElement;
    }
}
