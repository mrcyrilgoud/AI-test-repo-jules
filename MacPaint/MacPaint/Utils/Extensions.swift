import SwiftUI

extension View {
    func renderAsImage() -> NSImage? {
        let view = NoopView()
        let controller = NSHostingController(rootView: self.body(in: view))
        let targetSize = controller.view.intrinsicContentSize
        controller.view.bounds = CGRect(origin: .zero, size: targetSize)
        controller.view.layout()
        let bitmap = controller.view.bitmapImageRepForCachingDisplay(in: controller.view.bounds)
        bitmap?.size = controller.view.bounds.size
        controller.view.cacheDisplay(in: controller.view.bounds, to: bitmap!)
        let image = NSImage(size: targetSize)
        image.addRepresentation(bitmap!)
        return image
    }
}

private struct NoopView: View {
    var body: some View {
        EmptyView()
    }
}

private extension View {
    func body(in v: NoopView) -> some View {
        body
            .environment(\.self, v.environment)
            .environmentObject(v.environmentObject)
    }
}
