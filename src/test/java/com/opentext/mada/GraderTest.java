package com.opentext.mada;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;


public class GraderTest {
    @Test
   public void fiftyNineShouldReturnF () {
        Grader grader = new Grader();
        assertEquals('F',grader.determineLetterGrade(59));
    }

    @Test
    public void sixtyNineShouldReturnD () {
        Grader grader = new Grader();
        assertEquals('D',grader.determineLetterGrade(69));
    }

    @Test
    @Disabled
    public void seventyNineShouldReturnC () {
        Grader grader = new Grader();
        assertEquals('C',grader.determineLetterGrade(79));
    }

    @Test
    public void eightyNineShouldReturnB () {
        Grader grader = new Grader();
        assertEquals('B',grader.determineLetterGrade(89));
    }

    @Test
    public void ninetyNineShouldReturnA () {
        Grader grader = new Grader();
        assertEquals('A',grader.determineLetterGrade(99));
    }

    @Test
    public void eightyShouldReturnB () {
        Grader grader = new Grader();
        assertEquals('B',grader.determineLetterGrade(80));
    }

    @Test
    public void negativeOneShouldReturnIllegalArgumentException() {
        Grader grader = new Grader();
        assertThrows(IllegalArgumentException.class, () -> {
            grader.determineLetterGrade(-1);
        });
    }

    @Test
    public void parameterCase() {
        Grader grader = new Grader();
        assertEquals(System.getProperty("param"),String.valueOf(grader.determineLetterGrade(80)));

    }

    @Test
    public void environmentCase() {
        Grader grader = new Grader();
        System.out.println(System.getProperty("ENV"));
    }

    @Test
    public void $data_Driven_Properties() {
        Grader grader = new Grader();
        System.out.println(System.getProperty("DataSet1"));
    }

    @Test
    public void _predefinedParameters() {
        Grader grader = new Grader();
        System.out.println(System.getProperty("#sctm_keywords"));
        System.out.println(System.getProperty("SILK Test Name"));

    }

    @Test
    public void systemParameters() {
        Grader grader = new Grader();
        System.out.println(System.getProperty("#sctm_execdef_name"));
        System.out.println(System.getProperty("#sctm_product"));
        System.out.println(System.getProperty("#sctm_test_name"));
        System.out.println(System.getProperty("#sctm_test_id"));

    }

}
