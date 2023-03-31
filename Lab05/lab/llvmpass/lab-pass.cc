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
using namespace llvm;


char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Function &F)
{
  for (auto &BB : F) {
    errs() << F.getName() << "\n";
    errs() << BB << "\n";
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

const char* getSpace(int num) {
    std::string str;
    for(int i = 0; i < num; i++) {
        str += " ";
    }
    std::cout << "|" << str << "|" << std::endl;
    return str.c_str();
}

bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";
  for (auto &F : M) {
    if (F.empty()) 
      continue;

    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();
    Instruction *Istart = &(Bstart.front());  // Get the first instruction in the first BB

    // std::cout << getDepth(M, F) << std::endl;

    std::string str = F.getName().str() + ": ";
    Constant *funcName = getI8StrVal(M, str.c_str(), "funcName");  // Cast to c string
    // Constant *space = getI8StrVal(M, getSpace(getDepth(M, F)), "space");
    Constant *funcAddr = ConstantExpr::getBitCast(&F, Type::getInt8PtrTy(M.getContext()));
    Constant *newLine = getI8StrVal(M, "\n", "newline");

    FunctionCallee printfCallee = printfPrototype(M);    
    IRBuilder<> Builder(Istart);
    Builder.CreateCall(printfCallee, {funcName} );
    // Builder.CreateCall(printfCallee, {space} );
    Builder.CreateCall(printfCallee, {funcAddr} );
    Builder.CreateCall(printfCallee, {newLine});
    
    dumpIR(F);
  }
  
  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);