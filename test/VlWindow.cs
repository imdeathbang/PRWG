using System.Runtime.InteropServices;
using System.Runtime.CompilerServices;

public partial class VlWindow {

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix")]
    private static partial int vlGetWindowWidth(
        IntPtr window
    );

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix")]
    private static partial void vlSetWindowWidth(
        IntPtr window,
        int width
    );

    public VlWindow(string title) {
    }
}