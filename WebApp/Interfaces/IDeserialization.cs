namespace WebApp.Interfaces;

using System.Text.Json;
public interface IDeserialization<Self> where Self : IDeserialization<Self>
{
    static abstract public Self FromJson(JsonElement json);
}
