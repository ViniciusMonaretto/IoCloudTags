export class User
{
    Id: Number
    Name: string
    Email: string
    PhoneNumber: string
    Type: Number
    Rfid: string
    Password: string

    constructor(name: string, email: string, phoneNumber: string, type: Number, Rfid: string, Id: number)
    {
        this.Name = name
        this.Email = email
        this.PhoneNumber = phoneNumber
        this.Rfid = Rfid
        this.Type = type
        this.Password = ""
        this.Id = Id
    }
}