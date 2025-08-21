using Microsoft.AspNetCore.Mvc;
using System.Text.Json.Serialization;
namespace WebApp.Models.Requests;
/// <summary>
/// Class defines a basic template for any JSON response that will be sent or
/// received by the server.
/// </summary>
public abstract class ApiMessage<Type>
{
    public UInt64 _id = 0x7FFFFFFFFFFFFFFF;
    public String _sender = "";
    public String _receiver = "";
    public String _timestamp = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss");
    public MessageStatus _status = MessageStatus.Pending;
    public Type _content;

    public ApiMessage(
            String sender,
            String receiver,
            Type content
            )
    {
        _sender = sender;
        _receiver = receiver;
        _content = content;
    }

    /// <summary>
    /// Identifier for a message. 
    /// </summary>
    public virtual UInt64 Id
    {
        get => _id;
        set
        {
            if (value >= 0)
            {
                _id = value;
            }
        }
    }

    /// <summary>
    /// Tells us if the response has been successfully sent or received.
    /// </summary>
    [JsonConverter(typeof(JsonStringEnumConverter))]
    public virtual MessageStatus Status
    {
        get => _status;
        set
        {
            _status = value;

        }
    }

    /// <summary>
    /// Who sent the message. 
    /// </summary>
    public virtual String Sender
    {
        get => _sender;
        set
        {
            _sender = value;
        }
    }

    /// <summary>
    /// Who will receive the message. 
    /// </summary>
    public virtual String Receiver
    {
        get => _receiver;
        set
        {
            _receiver = value;
        }
    }

    /// <summary>
    /// When was the message sent or received. 
    /// </summary>
    public virtual String Timestamp
    {
        get => _timestamp;
    }

    /// <summary> 
    /// This function should be used to verify the entire class before
    /// serializing to a JSON. 
    /// </summary>
    public virtual bool Validate()
    {
        bool checkSender = Sender.Length > 0 ? true : false;
        bool checkReceiver = Receiver.Length > 0 ? true : false;
        return checkSender && checkReceiver;
    }

    /// <summary> 
    /// Return the content of the class.
    /// </summary>
    public virtual Type Content
    {
        get => _content;
        set { _content = value; }
    }
}


public enum MessageStatus
{
    Success = 0,
    Failure = 1,
    Pending = 2,
}
