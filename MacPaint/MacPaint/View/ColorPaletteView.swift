import SwiftUI

struct ColorPaletteView: View {
    @ObservedObject var viewModel: DrawingViewModel
    let colors: [Color] = [.red, .orange, .yellow, .green, .blue, .purple, .black, .white]

    var body: some View {
        HStack {
            ForEach(colors, id: \.self) { color in
                Button(action: { viewModel.selectedColor = color }) {
                    Rectangle()
                        .foregroundColor(color)
                        .frame(width: 30, height: 30)
                }
            }
        }
    }
}
