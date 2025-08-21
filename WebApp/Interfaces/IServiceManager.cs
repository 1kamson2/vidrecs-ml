namespace WebApp.Interfaces;

using WebApp.Models.Requests;
using WebApp.Models.Responses;

public interface IServiceManager<Self> where Self : IServiceManager<Self>
{
    Task<LoginResponse?> LoginAttempt(LoginRequest request);
    Task<RegisterResponse?> RegisterAttempt(RegisterRequest request);
    Task<String?> GameInfoFetchAttempt(GameRequest request);
}
