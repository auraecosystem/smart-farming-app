module SocketPipelineServer

open System
open System.Buffers
open System.IO.Pipelines
open System.Net
open System.Net.Sockets
open System.Text
open System.Threading.Tasks

// --- STAGE 1: SOCKET TO PIPE WRITER ---

let fillPipeAsync (socket: Socket) (writer: PipeWriter) : Task = task {
    let minimumBufferSize = 512
    let mutable isRunning = true

    while isRunning do
        // 1. Lease memory directly from the pipeline pool
        let memory = writer.GetMemory(minimumBufferSize)

        try
            // 2. Receive bytes straight into the leased Memory<byte> buffer
            let! bytesRead = socket.ReceiveAsync(memory, SocketFlags.None).AsTask()

            if bytesRead = 0 then
                // Socket closed gracefully by client
                isRunning <- false
            else
                // 3. Inform the pipe how many bytes were written and flush to the reader
                writer.Advance(bytesRead)
                let! result = writer.FlushAsync()
                if result.IsCompleted then
                    isRunning <- false

        with :? SocketException as ex ->
            printfn "[Socket Error] %s" ex.Message
            isRunning <- false

    // Complete the writer to signal the reader to finish
    do! writer.CompleteAsync()
}

// --- STAGE 2: PIPE READER TO PROTOCOL PARSER ---

let tryReadLine (buffer: byref<ReadOnlySequence<byte>>) (lineSlice: byref<ReadOnlySequence<byte>>) : bool =
    let positionOption = buffer.PositionOf(byte '\n')
    match positionOption with
    | Nullable pos ->
        lineSlice <- buffer.Slice(0, pos)
        buffer <- buffer.Slice(buffer.GetPosition(1L, pos))
        true
    | _ -> false

let readPipeAsync (reader: PipeReader) : Task = task {
    let mutable isCompleted = false

    while not isCompleted do
        let! result = reader.ReadAsync()
        let mutable buffer = result.Buffer
        isCompleted <- result.IsCompleted

        let mutable lineSlice = ReadOnlySequence<byte>()

        // Extract and process all complete lines delimited by '\n'
        while tryReadLine (&buffer) (&lineSlice) do
            // Slice to span for zero-copy inspection
            let payloadSpan = lineSlice.ToSpan()
            let message = Encoding.UTF8.GetString(payloadSpan)
            printfn "[Server Received] %s" (message.TrimEnd('\r'))

        // Advance reader position:
        // - 'buffer.Start' indicates consumed data (freed from memory pool)
        // - 'buffer.End' indicates unparsed data (preserved for next read iteration)
        reader.AdvanceTo(buffer.Start, buffer.End)

    do! reader.CompleteAsync()
}

// --- CONNECTION HANDLER ---

let processConnectionAsync (socket: Socket) : Task = task {
    use socket = socket
    let pipe = Pipe()

    // Run socket ingestion and payload parsing concurrently
    let fillTask = fillPipeAsync socket pipe.Writer
    let readTask = readPipeAsync pipe.Reader

    do! Task.WhenAll(fillTask, readTask)
    printfn "[Server] Client disconnected and pipeline closed."
}

// --- SERVER DRIVER ---

let startServerAsync (ip: string) (port: int) : Task = task {
    let listenSocket = new Socket(SocketType.Stream, ProtocolType.Tcp)
    listenSocket.Bind(IPEndPoint(IPAddress.Parse(ip), port))
    listenSocket.Listen(128)

    printfn "[Server Listening] TCP %s:%d" ip port

    while true do
        let! clientSocket = listenSocket.AcceptAsync()
        printfn "[Server] Client connected from %O" clientSocket.RemoteEndPoint
        // Fire and forget handling per client connection
        let _ = processConnectionAsync clientSocket
        ()
}

// --- ENTRY POINT ---

[<EntryPoint>]
let main _ =
    // Run server on 0.0.0.0:9494
    let serverTask = startServerAsync "127.0.0.1" 0000
    serverTask.GetAwaiter().GetResult()
    0
