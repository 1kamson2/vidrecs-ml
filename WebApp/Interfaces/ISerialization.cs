namespace WebApp.Interfaces;

public interface ISerialization<Self> where Self : ISerialization<Self>
{
    public StringContent ToJson();
}
