export class User
{
    Name: string
    Email: string
    PhoneNumber: string
    Type: Number
    Rfid: string

    constructor(name: string, email: string, phoneNumber: string, type: Number, Rfid: string)
    {
        this.Name = name
        this.Email = email
        this.PhoneNumber = phoneNumber
        this.Rfid = Rfid
        this.Type = type
    }
}