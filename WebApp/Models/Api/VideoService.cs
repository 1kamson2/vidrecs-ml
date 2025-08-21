namespace WebApp.Models.Api;

using WebApp.Models.Requests;
using WebApp.Models.Responses;
using WebApp.Interfaces;

using System.Text.Json;

public class ServiceManager : IServiceManager<ServiceManager>
{
    private HttpClient _httpClient;
    public ServiceManager(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<LoginResponse?> LoginAttempt(LoginRequest request)
    {
        // Serialize the C# object to a JSON string
        HttpResponseMessage? response = await _httpClient.PostAsync(
                "api/login",
                request.ToJson()
                );

        if (!response.IsSuccessStatusCode) { return null; }

        String content = await response.Content.ReadAsStringAsync();
        if (content is null) { return null; }

        JsonElement? json = LoginResponse.ReadHttpContent(content);
        return json.HasValue ? LoginResponse.FromJson(json.Value) : null;
    }

    public async Task<RegisterResponse?> RegisterAttempt(RegisterRequest request)
    {
        // Serialize the C# object to a JSON string
        HttpResponseMessage? response = await _httpClient.PostAsync(
                "api/register",
                request.ToJson()
                );
        if (!response.IsSuccessStatusCode) { return null; }
        String content = await response.Content.ReadAsStringAsync();
        if (content is null) { return null; }

        JsonElement? json = RegisterResponse.ReadHttpContent(content);
        return json.HasValue ? RegisterResponse.FromJson(json.Value) : null;
    }

    async public Task<String?> GameInfoFetchAttempt(GameRequest request)
    {
        // Serialize the C# object to a JSON string
        HttpResponseMessage? response = await _httpClient.PostAsync(
                "api/request_game",
                request.ToJson()
                );

        if (!response.IsSuccessStatusCode) { return null; }
        String content = await response.Content.ReadAsStringAsync();
        return content is null ? null : content;
    }
}
