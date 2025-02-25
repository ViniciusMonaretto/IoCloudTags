export class Event
{
    LocationId: Number
    UserId: Number
    BeginDate: Date
    EndDate: Date

    constructor(locationId: Number, userId: Number, beginDate: Date, endDate: Date)
    {
        this.UserId = userId
        this.LocationId = locationId
        this.BeginDate = beginDate
        this.EndDate = endDate
    }
}