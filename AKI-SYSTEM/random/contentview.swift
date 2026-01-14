import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    @FocusState private var isInputFocused: Bool
    
    var body: some View {
        ZStack {
            // Deep blue-purple gradient background like your design
            LinearGradient(
                colors: [
                    Color(red: 0.15, green: 0.20, blue: 0.35),
                    Color(red: 0.10, green: 0.15, blue: 0.30)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Title bar
                TitleBarView()
                    .environmentObject(appState)
                
                // Main terminal area with chat history
                TerminalAreaView(isInputFocused: _isInputFocused)
                    .environmentObject(appState)
                
                Spacer()
                
                // Bottom controls (4 boxes + user settings)
                BottomControlsView()
                    .environmentObject(appState)
            }
            .padding(20)
        }
        .onAppear {
            isInputFocused = true
        }
    }
}

// Title Bar
struct TitleBarView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        HStack {
            // Left side - circular decorations (like macOS window controls)
            HStack(spacing: 8) {
                Circle()
                    .fill(Color.red.opacity(0.3))
                    .frame(width: 12, height: 12)
                Circle()
                    .fill(Color.yellow.opacity(0.3))
                    .frame(width: 12, height: 12)
                Circle()
                    .fill(Color.green.opacity(0.3))
                    .frame(width: 12, height: 12)
            }
            
            Spacer()
            
            // Title
            Text("AKISYSTEM > H@CKY > SIZE")
                .font(.system(size: 16, weight: .semibold, design: .monospaced))
                .foregroundColor(.white.opacity(0.9))
                .tracking(2)
            
            Spacer()
            
            // Right side - Example label
            Text("EXAMPLE = LLAMA")
                .font(.system(size: 11, design: .monospaced))
                .foregroundColor(.white.opacity(0.6))
        }
        .padding(.horizontal, 15)
        .padding(.vertical, 12)
    }
}

// Main Terminal Area
struct TerminalAreaView: View {
    @EnvironmentObject var appState: AppState
    @FocusState var isInputFocused: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Terminal header info
            HStack {
                Text("Last login: \(getCurrentTimeString()) on ttys000")
                    .font(.system(size: 11, design: .monospaced))
                    .foregroundColor(.white.opacity(0.5))
                Spacer()
            }
            .padding(.horizontal, 15)
            .padding(.vertical, 8)
            
            // Chat/Terminal scrollable area
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 8) {
                        // Output lines
                        ForEach(appState.outputLines) { line in
                            OutputLineView(line: line)
                                .id(line.id)
                        }
                        
                        // Current input line with prompt
                        HStack(spacing: 6) {
                            Text(">>>")
                                .foregroundColor(.white.opacity(0.7))
                            
                            TextField("", text: $appState.inputText)
                                .textFieldStyle(.plain)
                                .foregroundColor(.white)
                                .focused($isInputFocused)
                                .onSubmit {
                                    if !appState.inputText.isEmpty {
                                        appState.executeCommand(appState.inputText)
                                        appState.inputText = ""
                                    }
                                }
                        }
                        .font(.system(size: 13, design: .monospaced))
                        .padding(.horizontal, 15)
                        .id("input")
                    }
                    .padding(.vertical, 10)
                }
                .onChange(of: appState.outputLines.count) { _ in
                    withAnimation {
                        proxy.scrollTo("input", anchor: .bottom)
                    }
                }
            }
            .frame(minHeight: 300)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.black.opacity(0.4))
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.blue.opacity(0.3), lineWidth: 1)
                    )
            )
            
            // "CHAT/TERMINAL FONT" label
            Text("CHAT/TERMINAL FONT")
                .font(.system(size: 24, weight: .medium, design: .monospaced))
                .foregroundColor(.red.opacity(0.6))
                .italic()
                .padding(.top, 15)
                .padding(.leading, 15)
        }
    }
    
    func getCurrentTimeString() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "EEE MMM dd HH:mm:ss"
        return formatter.string(from: Date())
    }
}

// Output Line
struct OutputLineView: View {
    let line: OutputLine
    
    var body: some View {
        Text(line.text)
            .font(.system(size: 13, design: .monospaced))
            .foregroundColor(colorForType(line.type))
            .padding(.horizontal, 15)
            .textSelection(.enabled)
    }
    
    func colorForType(_ type: OutputType) -> Color {
        switch type {
        case .normal:
            return .white.opacity(0.9)
        case .command:
            return Color(red: 0.6, green: 1.0, blue: 0.6)
        case .response:
            return Color(red: 0.5, green: 0.8, blue: 1.0)
        case .info:
            return .cyan.opacity(0.8)
        case .error:
            return .red
        case .warning:
            return .yellow
        }
    }
}

// Bottom Controls (4 boxes + user settings)
struct BottomControlsView: View {
    @EnvironmentObject var appState: AppState
    @State private var showUserSettings = false
    
    var body: some View {
        HStack(spacing: 15) {
            // 1. PERSONA box
            SelectionBox(
                title: "PERSONA",
                subtitle: "CHOOSE PERSONA FROM LIST",
                currentValue: appState.currentPersona,
                options: appState.personas,
                onSelect: { appState.currentPersona = $0 }
            )
            
            // 2. TONE box
            SelectionBox(
                title: "TONE",
                subtitle: "CHOOSE TONE",
                currentValue: appState.currentTone,
                options: appState.tones,
                onSelect: { appState.currentTone = $0 }
            )
            
            // 3. OUTPUT box
            SelectionBox(
                title: "OUTPUT",
                subtitle: "SIZE OF OUTPUT",
                currentValue: appState.currentOutput,
                options: appState.outputs,
                onSelect: { appState.currentOutput = $0 }
            )
            
            // 4. MODEL box
            VStack(alignment: .leading, spacing: 4) {
                Text("MODEL")
                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                    .foregroundColor(.red.opacity(0.8))
                
                Text(appState.modelName)
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(.white.opacity(0.7))
                
                Text("MISTRAL DEEPSEEK...ETC")
                    .font(.system(size: 8, design: .monospaced))
                    .foregroundColor(.white.opacity(0.5))
            }
            .frame(width: 140, height: 80)
            .padding(8)
            .background(
                RoundedRectangle(cornerRadius: 4)
                    .stroke(Color.red.opacity(0.6), lineWidth: 2)
            )
            
            Spacer()
            
            // USER SETTINGS box (right side)
            Button(action: {
                showUserSettings.toggle()
            }) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("USER SETTINGS")
                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                        .foregroundColor(.red.opacity(0.8))
                    
                    Text("VERSION = 0.1 A")
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundColor(.white.opacity(0.6))
                    
                    Text("LANGUAGES = FR / EN")
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundColor(.white.opacity(0.6))
                }
                .frame(width: 180, height: 80)
                .padding(8)
                .background(
                    RoundedRectangle(cornerRadius: 4)
                        .stroke(Color.red.opacity(0.6), lineWidth: 2)
                )
            }
            .buttonStyle(.plain)
            .sheet(isPresented: $showUserSettings) {
                UserSettingsView()
                    .environmentObject(appState)
            }
        }
        .padding(.top, 15)
    }
}

// Reusable Selection Box
struct SelectionBox: View {
    let title: String
    let subtitle: String
    let currentValue: String
    let options: [String]
    let onSelect: (String) -> Void
    
    var body: some View {
        Menu {
            ForEach(options, id: \.self) { option in
                Button(action: {
                    onSelect(option)
                }) {
                    HStack {
                        Text(option)
                        if option == currentValue {
                            Image(systemName: "checkmark")
                        }
                    }
                }
            }
        } label: {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                    .foregroundColor(.red.opacity(0.8))
                
                Text(currentValue.uppercased())
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(.white.opacity(0.7))
                
                Text(subtitle)
                    .font(.system(size: 8, design: .monospaced))
                    .foregroundColor(.white.opacity(0.5))
            }
            .frame(width: 120, height: 80)
            .padding(8)
            .background(
                RoundedRectangle(cornerRadius: 4)
                    .stroke(Color.red.opacity(0.6), lineWidth: 2)
            )
        }
        .menuStyle(.borderlessButton)
    }
}

// User Settings Panel
struct UserSettingsView: View {
    @EnvironmentObject var appState: AppState
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        VStack(spacing: 20) {
            Text("USER SETTINGS")
                .font(.system(size: 18, weight: .bold, design: .monospaced))
                .foregroundColor(.white)
            
            Form {
                Section("Model Configuration") {
                    TextField("Model Name", text: $appState.modelName)
                    TextField("Local Server", text: $appState.localServer)
                    TextField("Remote Server", text: $appState.remoteServer)
                }
                
                Section("Display") {
                    Toggle("Show Timestamps", isOn: .constant(true))
                    Toggle("Color Output", isOn: .constant(true))
                }
            }
            .formStyle(.grouped)
            
            Button("Close") {
                dismiss()
            }
            .buttonStyle(.borderedProminent)
        }
        .frame(width: 400, height: 500)
        .padding()
        .background(Color(red: 0.1, green: 0.1, blue: 0.15))
    }
}

// Preview
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(AppState())
            .frame(width: 1000, height: 700)
    }
}