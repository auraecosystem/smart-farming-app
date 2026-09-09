open System
open System.Buffers.Binary
open System.Text

// --- PACKET LAYOUT ---
// [ 0..1 ] Magic Bytes (0x41, 0x55)
// [ 2..5 ] Sequence ID (uint32, Big-Endian)
// [ 6..7 ] Topic Length (uint16, Big-Endian)
// [ 8..N ] Topic String (UTF-8)
// [ N..M ] Payload (Raw Bytes)

[<Struct>]
type PacketHeader = {
    SequenceId: uint32
    TopicLength: uint16
    PayloadLength: int
}

module ZeroCopyParser =

    /// Parse header directly from a ReadOnlySpan without heap allocations
    let tryParseHeader (buffer: ReadOnlySpan<byte>, [<System.Runtime.InteropServices.Out>] header: byref<PacketHeader>) : bool =
        if buffer.Length < 8 then
            false
        else
            let magic = BinaryPrimitives.ReadUInt16BigEndian(buffer.Slice(0, 2))
            if magic <> 0x4155us then // 'AU' magic bytes
                false
            else
                let seqId = BinaryPrimitives.ReadUInt32BigEndian(buffer.Slice(2, 4))
                let topicLen = BinaryPrimitives.ReadUInt16BigEndian(buffer.Slice(6, 2))
                let payloadLen = buffer.Length - 8 - int topicLen

                if payloadLen < 0 then
                    false
                else
                    header <- { SequenceId = seqId; TopicLength = topicLen; PayloadLength = payloadLen }
                    true

    /// Extract packet slices zero-copy using ReadOnlySpan
    let processFrame (buffer: ReadOnlySpan<byte>) =
        let mutable header = Unchecked.defaultof<PacketHeader>
        
        if tryParseHeader(buffer, &header) then
            // Slice topic string without array allocation
            let topicSpan = buffer.Slice(8, int header.TopicLength)
            
            // Slice payload without array allocation
            let payloadSpan = buffer.Slice(8 + int header.TopicLength, header.PayloadLength)

            printfn "[Zero-Copy Header] Seq ID: %d | Payload Size: %d bytes" header.SequenceId payloadSpan.Length
            
            // Optional zero-allocation UTF-8 string output directly to stdout/destination buffer
            let topicStr = Encoding.UTF8.GetString(topicSpan)
            printfn "  -> Topic: %s" topicStr
            printfn "  -> First Payload Byte: 0x%X" payloadSpan.[0]
        else
            printfn "[Parser Error] Invalid or truncated buffer frame"

// --- DEMONSTRATION WITH STACK ALLOCATION ---

[<EntryPoint>]
let main _ =
    // Create stack-allocated or pinned buffer
    let rawBuffer = stackalloc byte 32
    
    // Construct mock frame: Magic (0x4155), SeqId (1001), TopicLen (4), Topic ("data"), Payload (0xFF, 0xAA)
    rawBuffer.[0] <- 0x41b; rawBuffer.[1] <- 0x55b
    BinaryPrimitives.WriteUInt32BigEndian(rawBuffer.Slice(2, 4), 1001u)
    BinaryPrimitives.WriteUInt16BigEndian(rawBuffer.Slice(6, 2), 4us)
    
    // Write topic "data" directly to span
    Encoding.UTF8.GetBytes("data".AsSpan(), rawBuffer.Slice(8, 4)) |> ignore
    
    // Write payload bytes
    rawBuffer.[12] <- 0xFFb
    rawBuffer.[13] <- 0xAAb

    // Execute zero-allocation parse over the span slice
    let frameSpan = ReadOnlySpan<byte>(NativePtr.toVoidPtr rawBuffer, 14)
    ZeroCopyParser.processFrame frameSpan

    0
