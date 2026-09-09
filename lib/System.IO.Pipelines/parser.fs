open System
open System.Buffers
open System.IO.Pipelines
open System.Text
open System.Threading.Tasks

module PipelineParser =

    /// Stage 1: Async Writer - Pushes raw network/stream data into the Pipe
    let writeDataAsync (writer: PipeWriter) (dataChunks: byte[][] ) : Task = task {
        for chunk in dataChunks do
            // 1. Request memory buffer from the pool
            let memory = writer.GetMemory(chunk.Length)
            
            // 2. Copy data directly into the pipeline memory span
            chunk.AsSpan().CopyTo(memory.Span)
            
            // 3. Advance the writer position and flush
            writer.Advance(chunk.Length)
            let! _ = writer.FlushAsync()
            
            // Simulate network arrival delay
            do! Task.Delay(50)

        // Mark writing as completed
        do! writer.CompleteAsync()
    }

    /// Helper: Parses lines separated by '\n' (0x0A) from a ReadOnlySequence without heap allocations
    let tryReadLine (sequence: byref<ReadOnlySequence<byte>>) (lineSlice: byref<ReadOnlySequence<byte>>) : bool =
        let positionOption = sequence.PositionOf(byte '\n')
        match positionOption with
        | Nullable pos ->
            // Extract line slice up to the delimiter
            lineSlice <- sequence.Slice(0, pos)
            // Advance the main sequence buffer past the delimiter
            sequence <- sequence.Slice(sequence.GetPosition(1L, pos))
            true
        | _ -> 
            false

    /// Stage 2: Async Reader - Parses incoming frames from the Pipe
    let readDataAsync (reader: PipeReader) : Task = task {
        let mutable isCompleted = false

        while not isCompleted do
            // 1. Read available data from the pipe
            let! result = reader.ReadAsync()
            let mutable buffer = result.Buffer
            isCompleted <- result.IsCompleted

            let mutable lineSlice = ReadOnlySequence<byte>()

            // 2. Parse all complete lines in the current buffer slice
            while tryReadLine (&buffer) (&lineSlice) do
                let lineString = Encoding.UTF8.GetString(lineSlice.ToSpan())
                printfn "[Parsed Frame] %s" lineString

            // 3. Tell the Pipe how much data was consumed vs examined
            // Data before 'buffer.Start' is freed; remaining unparsed data is retained for the next read
            reader.AdvanceTo(buffer.Start, buffer.End)

        // Mark reading as completed
        do! reader.CompleteAsync()
    }

// --- EXECUTION DRIVER ---

[<EntryPoint>]
let main _ =
    let pipe = Pipe()

    let mockStreamData = [|
        Encoding.UTF8.GetBytes("FRAME_1: INIT\nFRAME_2: PROCES")
        Encoding.UTF8.GetBytes("SING_DATA\nFRAME_3: END\n")
    |]

    // Run Writer and Reader concurrently
    let writerTask = PipelineParser.writeDataAsync pipe.Writer mockStreamData
    let readerTask = PipelineParser.readDataAsync pipe.Reader

    Task.WaitAll(writerTask, readerTask)
    0
