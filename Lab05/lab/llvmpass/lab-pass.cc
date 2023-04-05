/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"

#include <random>
#include <iostream>
#include <string>
#include <vector>
using namespace llvm;
using namespace std;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Module &M)
{
    errs() << "\n\n---- dumpIR ----\n";
  for (auto &F : M) {      
    errs() << F.getName() << "\n";
    for (auto &BB : F) {
        errs() << BB << "\n";
    }
  }
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}


bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";
  LLVMContext &ctx = M.getContext();

  for (auto &F : M) {
    if (F.empty()) 
      continue;

    errs() << "\n ------------------- \n" << F << "\n ------------------- \n";

    BasicBlock &Bstart = F.front();
    Instruction &Istart = Bstart.front();  // Get the first instruction in the first BB
    FunctionCallee printfCallee = printfPrototype(M);
    IRBuilder<> Builder(&Istart);

    // Cast the function address to an integer type
    Type *IntPtrTy = Type::getIntNTy(ctx, sizeof(void*) * 8);

    // Get the function address as a void pointer
    Constant *funcAddr = ConstantExpr::getBitCast(&F, Type::getInt8PtrTy(ctx));

    // Cast the function address to an integer type
    Constant *funcAddrInt = ConstantExpr::getPtrToInt(funcAddr, IntPtrTy);

    // Create a format string for printf
    std::string formatStr = F.getName().str() + ": 0x%lx\n";
    Constant *formatCStr = getI8StrVal(M, formatStr.c_str(), "formatCStr");

    // Call printf with the function address as an argument

    Builder.CreateCall(printfCallee, {formatCStr, funcAddrInt});
  }
  dumpIR(M);
  
  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);