using System.Runtime.InteropServices;
using System.Runtime.CompilerServices;

namespace velix;

public partial class VlWindow {

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix", StringMarshalling = StringMarshalling.Utf16)]
    private static partial VlResult vlCreateWindow(
        string title,
        int width,
        out IntPtr handle
    );

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix")]
    private static partial void vlShowWindow(
        IntPtr window,
        [MarshalAs(UnmanagedType.I1)] bool show
    );

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix", StringMarshalling = StringMarshalling.Utf16)]
    private static partial string VlGetPip(
        IntPtr window
    );

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

    private IntPtr _handle;

    public VlWindow( 
        string title,
        int width
    ) {
        VlResult result = vlCreateWindow(title, width, out IntPtr handle);
        if (result != VlResult.VL_SUCCESS) {
            throw new InvalidOperationException(result.ToString());
        }
        _handle = handle;
    }
    public void VlShowWindow(
        bool show
    ) {
        vlShowWindow(_handle, show);
    }
    public string VlGetPip(

    ) {
        return vlGetPip(_handle);
    }
}