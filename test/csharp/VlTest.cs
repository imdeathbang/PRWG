using System.Runtime.InteropServices;
using System.Runtime.CompilerServices;

namespace velix;

public partial class VlTest {

    [UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]
    [LibraryImport("velix")]
    private static partial IntPtr vlCreateTest();

    private IntPtr _handle;

    public VlTest() {
        _handle = vlCreateTest();
        if (_handle == IntPtr.Zero) {
            throw new InvalidOperationException("Handle is NULL");
        }
    }


}
