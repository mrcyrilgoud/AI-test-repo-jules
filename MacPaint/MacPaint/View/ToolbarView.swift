import SwiftUI

struct ToolbarView: View {
    @ObservedObject var viewModel: DrawingViewModel

    var body: some View {
        HStack {
            Button(action: { viewModel.selectedTool = .pencil }) {
                Image(systemName: "pencil")
            }
            Button(action: { viewModel.selectedTool = .paintbrush }) {
                Image(systemName: "paintbrush")
            }
            Button(action: { viewModel.selectedTool = .eraser }) {
                Image(systemName: "eraser")
            }
            Button(action: { viewModel.selectedTool = .paintbucket }) {
                Image(systemName: "paintbucket")
            }
            Button(action: { viewModel.selectedTool = .line }) {
                Image(systemName: "line.diagonal")
            }
            Slider(value: $viewModel.selectedLineWidth, in: 1...20)

            Spacer()

            Button(action: {
                viewModel.importImage()
            }) {
                Image(systemName: "square.and.arrow.down")
            }

            Button(action: {
                let canvas = DrawingCanvas(viewModel: viewModel)
                viewModel.exportImage(view: canvas)
            }) {
                Image(systemName: "square.and.arrow.up")
            }
        }
    }
}
