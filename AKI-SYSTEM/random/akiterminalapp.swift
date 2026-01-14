import SwiftUI

@main
struct AKITerminalApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.hiddenTitleBar)
        .commands {
            CommandGroup(replacing: .newItem) {}
        }
    }
}

// App State Management
class AppState: ObservableObject {
    @Published var currentPersona: String = "core"
    @Published var currentTone: String = "neutral"
    @Published var currentOutput: String = "based"
    @Published var modelName: String = "deepseek"
    @Published var localServer: String = "localhost:11434"
    @Published var remoteServer: String = "-"
    @Published var outputLines: [OutputLine] = []
    @Published var inputText: String = ""
    @Published var commandHistory: [String] = []
    @Published var historyIndex: Int = -1
    
    let personas = ["core", "akademik", "shrink", "scientist", "journalist", 
                    "operator", "capitalist", "lawyer", "tourism", "whitehat"]
    let tones = ["neutral", "serious", "chill", "solemn", "happy", "sad"]
    let outputs = ["based", "concise", "precise", "developed"]
    
    func addOutput(_ text: String, type: OutputType = .normal) {
        outputLines.append(OutputLine(text: text, type: type))
    }
    
    func executeCommand(_ command: String) {
        // Add to history
        commandHistory.append(command)
        historyIndex = commandHistory.count
        
        // Add command to output
        let prompt = "h@cky/\(currentPersona) (\(currentTone)) → "
        addOutput(prompt + command, type: .command)
        
        // Process command (integrate with Python backend)
        processAKICommand(command)
    }
    
    func processAKICommand(_ command: String) {
        // System commands
        let cmd = command.lowercased().trimmingCharacters(in: .whitespaces)
        
        switch cmd {
        case "help":
            showHelp()
        case "personas":
            showPersonas()
        case "status":
            showStatus()
        case "clear":
            outputLines.removeAll()
        case "exit", "quit":
            NSApplication.shared.terminate(nil)
        default:
            // Call Python backend
            callPythonBackend(command)
        }
    }
    
    func showHelp() {
        let helpText = """
        
        === h@cky COMMAND REFERENCE ===
        
        SYNTAX:
          >command< /persona (tone) [output] content
        
        COMMANDS:
          >explain<       Use metaphor to explain
          >find<          Quick internet search
          >investigate<   Deep investigation
          >bamn<          By any means necessary
        
        PERSONAS:
          /akademik   /shrink   /scientist
          /journalist /operator /capitalist
        
        TONES: (serious) (chill) (solemn)
        OUTPUT: [concise] [precise] [based]
        
        SYSTEM: help, personas, status, clear, exit
        """
        addOutput(helpText, type: .info)
    }
    
    func showPersonas() {
        let text = """
        
        === AVAILABLE PERSONAS ===
        
        📚 /akademik    - Academic/pedagogical
        🧠 /shrink      - Mental health support
        🔬 /scientist   - Coding/development
        📰 /journalist  - Fact-checking
        ⚡ /operator    - Fast response
        💰 /capitalist  - Economic analysis
        ⚖️  /lawyer     - Legal guidance
        🛡️  /whitehat   - Ethical hacking (restricted)
        """
        addOutput(text, type: .info)
    }
    
    func showStatus() {
        let text = """
        
        === SYSTEM STATUS ===
        
        Persona:     \(currentPersona)
        Tone:        \(currentTone)
        Output Type: \(currentOutput)
        Model:       \(modelName)
        Server:      \(localServer)
        """
        addOutput(text, type: .info)
    }
    
    func callPythonBackend(_ command: String) {
        // This will call the Python aki_simple.py backend
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        
        // Path to your aki_simple.py
        let scriptPath = Bundle.main.resourcePath ?? ""
        process.arguments = [scriptPath + "/aki_backend.py", command, currentPersona, currentTone, currentOutput]
        
        let pipe = Pipe()
        process.standardOutput = pipe
        
        do {
            try process.run()
            process.waitUntilExit()
            
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            if let output = String(data: data, encoding: .utf8) {
                addOutput(output, type: .response)
            }
        } catch {
            addOutput("Error: \(error.localizedDescription)", type: .error)
        }
    }
}

// Output Line Model
struct OutputLine: Identifiable {
    let id = UUID()
    let text: String
    let type: OutputType
    let timestamp = Date()
}

enum OutputType {
    case normal
    case command
    case response
    case info
    case error
    case warning
}