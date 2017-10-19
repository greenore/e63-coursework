package edu.hu.e63.ML

import org.scalatra.test.scalatest._
import org.scalatest.FunSuiteLike

class e63LRTests extends ScalatraSuite with FunSuiteLike {

  addServlet(classOf[e63LR], "/*")

  test("GET / on e63LR should return status 200"){
    get("/"){
      status should equal (200)
    }
  }

}
