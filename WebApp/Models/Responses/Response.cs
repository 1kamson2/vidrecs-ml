namespace WebApp.Models.Responses;

using System.Text.Json;
using WebApp.Interfaces;
using WebApp.Models.Requests;


public sealed class Response : ApiMessage<String>, IDeserialization<Response>
{
    public Response(
            String sender,
            String receiver,
            String content
            ) : base(sender, receiver, content)
    { }

    static public Response FromJson(JsonElement json)
    {
        if (!json.TryGetProperty("id", out JsonElement id))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("sender", out JsonElement sender))
        {
            Console.WriteLine("do sth");

        }

        if (!json.TryGetProperty("recipient", out JsonElement receiver))
        {
            Console.WriteLine("do sth");
        }

        if (!json.TryGetProperty("content", out JsonElement content))
        {
            Console.WriteLine("do sth");
        }

        return new Response(
                sender.GetString(),
                receiver.GetString(),
                content.GetString()
                );
    }
}
