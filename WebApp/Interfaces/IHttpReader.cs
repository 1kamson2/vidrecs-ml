namespace WebApp.Interfaces;

using System.Text.Json;
public interface IHttpReader<Self> where Self : IHttpReader<Self>
{
    static abstract public JsonElement? ReadHttpContent(String content);
}
