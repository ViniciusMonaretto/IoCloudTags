export class Location
{
    Name: string
    Block: Number
    Sector: Number
    GatewayUUID: string
    ManagerId: Number
    Id: Number

    constructor(name: string, block: Number, sector: Number, gatewayUUID: string, managerId: Number, Id: number)
    {
        this.Name = name
        this.Block = block
        this.Sector = sector
        this.GatewayUUID = gatewayUUID
        this.ManagerId = managerId
        this.Id = Id
    }
}