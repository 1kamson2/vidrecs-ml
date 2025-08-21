namespace WebApp.Models.Requests;

using WebApp.Models.Forms;
using System.Text.Json;
using WebApp.Interfaces;

public class GameRequest : ApiMessage<GameForm>, IDeserialization<GameRequest>, ISerialization<GameRequest>
{
    public GameRequest(
            String sender,
            String receiver,
            GameForm videoForm
            ) : base(sender, receiver, videoForm) { }

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

    public static GameRequest FromJson(JsonElement json)
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

        GameForm form = GameForm.FromJson(content);

        return new GameRequest(
                sender.GetString(),
                receiver.GetString(),
                form
                );
    }

}
