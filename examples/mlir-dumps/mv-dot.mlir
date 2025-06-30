module {

  func.func @matvec(%A : tensor<?x?xf64>, %x : tensor<?xf64>, 
    %y_dst : tensor<?xf64>) -> tensor<?xf64> {

    %y = linalg.matvec ins(%A, %x: tensor<?x?xf64>, tensor<?xf64>) 
      outs(%y_dst : tensor<?xf64>) -> tensor<?xf64>

      return %y : tensor<?xf64>
  }


  func.func @dot(%x : tensor<?xf64>, %y : tensor<?xf64>) -> f64 {

    %alloc_res = tensor.empty() : tensor<f64>
    %dot = linalg.dot ins(%x, %y : tensor<?xf64>, tensor<?xf64>) 
      outs(%alloc_res : tensor<f64>) -> tensor<f64>

    %res = tensor.extract %dot[] : tensor<f64>
    return %res : f64
  }

  func.func @main(%A : tensor<?x?xf64>, %x : tensor<?xf64>, %y_dst :
  tensor<?xf64>) -> f64 {

    %Ax = func.call @matvec(%A, %x, %y_dst) { fuse_with = "dot" } : (tensor<?x?xf64>, tensor<?xf64>,
    tensor<?xf64>) -> tensor<?xf64>
    %res = func.call @dot(%Ax, %x) { fuse_with = "matvec" } : (tensor<?xf64>, tensor<?xf64>) -> f64

    return %res : f64
  }
}
