namespace WebApp.Models.Responses;

using System.Text.Json;
using WebApp.Interfaces;
using WebApp.Models.Requests;


public sealed class GameResponse : ApiMessage<List<String>>, IDeserialization<GameResponse>
{
    public GameResponse(
            String sender,
            String receiver,
            List<String> results
            ) : base(sender, receiver, results)
    { }

    static public GameResponse FromJson(JsonElement json)
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

        if (!json.TryGetProperty("content", out JsonElement content))
        {
            Console.WriteLine("do sth");
        }

        return new GameResponse(
                sender.GetString(),
                receiver.GetString(),
                content.EnumerateArray().Cast<String>().ToList<String>()
                );
    }

    static public JsonElement? ReadHttpContent(String content)
    {
        // TODO: Add error handling
        var jsonDoc = JsonDocument.Parse(content);
        return jsonDoc.RootElement;
    }
}
