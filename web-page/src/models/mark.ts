import { User } from "./user"
import { Location } from "./location"

export class Mark
{
    Id: Number
    User: User
    Location: Location
    UserName: string
    LocationName: string

    timestamp: String

    constructor(user: User, location: Location, timestamp: Date, Id: number)
    {
        this.User = user
        this.Location = location
        this.Id = Id

        this.UserName = this.User.Name
        this.LocationName = this.Location.Name
        this.timestamp = timestamp.toLocaleString()
    }
}