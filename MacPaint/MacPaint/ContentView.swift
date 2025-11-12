import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = DrawingViewModel()

    var body: some View {
        VStack {
            ToolbarView(viewModel: viewModel)
            DrawingCanvas(viewModel: viewModel)
            ColorPaletteView(viewModel: viewModel)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
